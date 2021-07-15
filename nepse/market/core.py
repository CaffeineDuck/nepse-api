import asyncio
import datetime
from typing import List, Optional

import humps

from nepse.errors import CompanyNotFound
from nepse.market.types import FloorSheet, MarketCap, MarketSummary, SectorwiseSummary
from nepse.utils import _ClientWrapperHTTPX, get

BASE_URL = "https://newweb.nepalstock.com/api/nots"


class MarketClient:
    def __init__(self, client_wrapper: _ClientWrapperHTTPX) -> None:
        self._client_wrapper = client_wrapper

    async def market_is_open(self) -> bool:
        """Checks if the market is open

        Returns:
            bool: Returns True if market is open and vice-versa
        """
        response = await self._client_wrapper._get_json(
            f"{BASE_URL}/nepse-data/market-open"
        )
        if response["isOpen"] != "CLOSE":
            return True
        return False

    async def check_IPO(self, scrip: str, BOID: int) -> bool:
        """Checks if the given user got the IPO

        Args:
            scrip (str): The Scrip of the company
            boid (int): The user's BOID

        Returns:
            bool: Returns if the user got alloted in the IPO
        """
        try:
            scripID = [
                resp.get("id")
                for resp in (
                    await self._client_wrapper._get_json(
                        "https://iporesult.cdsc.com.np/result/companyShares/fileUploaded"
                    )
                ).get("body")
                if resp.get("scrip") == scrip.upper()
            ][0]
        except IndexError:
            raise CompanyNotFound()

        return (
            await self._client_wrapper._post_json(
                url="https://iporesult.cdsc.com.np/result/result/check",
                body={"companyShareId": scripID, "boid": BOID},
            )
        ).get("success")

    async def get_market_caps(self) -> List[MarketCap]:
        """Returns the market caps which are sorted by date

        Returns:
            List[MarketCap]: Market Caps sorted by date
        """
        resp = await self._client_wrapper._get_json(
            f"{BASE_URL}/nepse-data/marcapbydate/?"
        )
        data = humps.decamelize(resp)
        return [MarketCap(**model) for model in data]

    async def get_floorsheets(
        self, sleep_time: Optional[int] = 0.4
    ) -> List[FloorSheet]:
        """Returns the floorsheet data for the current date

        .. note::

            Using this method may take upto **200** seconds, and may take upto **350** MB of memory.
            Use **get_floorsheets_raw** rather than this if you are planning to dumb the data.

        Args:
            sleep_time (int): The sleep time after each request so that we don't get
                rate limited. Increase this if you are getting `ServerDisconnected`

        Returns:
            List[FloorSheet]: List of floorsheet data in form of `FloorSheet`
        """
        contents = []

        pages = (
            (
                await self._client_wrapper._post_json_defualt_body(
                    f"{BASE_URL}/nepse-data/floorsheet?size=500"
                )
            )
            .get("floorsheets")
            .get("totalPages")
        )

        async def _create_model(data: dict) -> None:
            data = humps.decamelize(data)
            contents.append(FloorSheet(**data))

        async def _get_floorsheet_page(page_no: int) -> None:
            response = (
                (
                    await self._client_wrapper._post_json_defualt_body(
                        f"{BASE_URL}/nepse-data/floorsheet?page={page_no}&size=500&sort=contractId,desc"
                    )
                )
                .get("floorsheets")
                .get("content")
            )

            model_tasks = []
            for data in response:
                model_tasks.append(_create_model(data))

            await asyncio.gather(*model_tasks)

        for page_no in range(pages):
            await _get_floorsheet_page(page_no)
            await asyncio.sleep(sleep_time)

        return contents

    async def get_floorsheets_raw(self, sleep_time: Optional[int] = 0.4) -> List[dict]:
        """Returns raw floorsheet data which is faster than `nepse.MarketClient.get_floorsheets`

        .. note::

            Using this method may take upto **170** seconds, and may take upto **300** MB
            of memory. So only use it when necessary.

        Args:
            sleep_time (int): The sleep time after each request so that we don't get
                rate limited. Increase this if you are getting `ServerDisconnected`

        Returns:
            List[dict]: List of raw floorsheet objects
        """
        contents = []

        pages = (
            (
                await self._client_wrapper._post_json_defualt_body(
                    f"{BASE_URL}/nepse-data/floorsheet?size=500"
                )
            )
            .get("floorsheets")
            .get("totalPages")
        )

        async def _create_model(data: dict) -> None:
            contents.append(data)

        async def _get_floorsheet_page(page_no: int) -> None:
            response = (
                (
                    await self._client_wrapper._post_json_defualt_body(
                        f"{BASE_URL}/nepse-data/floorsheet?page={page_no}&size=500&sort=contractId,desc"
                    )
                )
                .get("floorsheets")
                .get("content")
            )

            model_tasks = [(_create_model(data)) for data in response]
            await asyncio.gather(*model_tasks)

        for page_no in range(pages):
            await _get_floorsheet_page(page_no)
            await asyncio.sleep(sleep_time)

        return contents

    async def get_sectorwise_summary(
        self, business_date: Optional[datetime.date] = None
    ) -> List[SectorwiseSummary]:
        """Get the sectorwise summary

        Args:
            business_date (Optional[datetime.date]): The date for which to fetch the data

        Returns:
            List[SectorwiseSummary]: The list containing data related to sector wise summary
        """
        business_date = business_date or datetime.date.today()

        sector_wise_summary = humps.decamelize(
            await self._client_wrapper._get_json(
                f"{BASE_URL}/sectorwise?businessDate={business_date}"
            )
        )

        return [SectorwiseSummary(**model) for model in sector_wise_summary]

    async def get_market_summaries(self) -> List[MarketSummary]:
        """Get the market summaries

        Returns:
            List[MarketSummary]: The list of Objects containing related to Market Summary
        """
        market_summary = humps.decamelize(
            await self._client_wrapper._get_json(f"{BASE_URL}/market-summary-history")
        )

        return [MarketSummary(**model) for model in market_summary]

    async def get_market_summary(
        self, date: Optional[datetime.date] = None
    ) -> MarketSummary:
        """Get the market summary for a specific date

        Args:
            date (Optional[datetime.date]): Date to filter the market summary. Defaults to today

        Returns:
            MarketSummary: [description]
        """
        market_summaries = await self.get_market_summaries()
        date = date or datetime.date.today()

        return get(market_summaries, business_date=date)
