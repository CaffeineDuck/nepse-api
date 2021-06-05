import asyncio
from typing import List

import humps

from nepse.market.types import FloorSheet, MarketCap
from nepse.utils import _ClientWrapperHTTPX

BASE_URL = "https://newweb.nepalstock.com/api/nots"
SPOOF_HEADER = {
    "authority": "newweb.nepalstock.com.np",
    "sec-ch-ua": "^\\^Google",
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://newweb.nepalstock.com.np/",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}


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

    async def check_IPO(self, scrip, boid) -> bool:
        """Checks if the given user got the IPO

        Args:
            scrip (Any): The Script
            boid (int): The boid

        Returns:
            bool: Returns if the user got alloted in the IPO
        """
        scripID = [
            resp["id"]
            for resp in self._client_wrapper._get_json(
                "https://iporesult.cdsc.com.np/result/companyShares/fileUploaded"
            )["body"]
            if resp["scrip"] == scrip.upper()
        ][0]

        return (
            await self._client_wrapper._post_json(
                url="https://iporesult.cdsc.com.np/result/result/check",
                body={"companyShareId": scripID, "boid": boid},
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

    async def get_floorsheets(self) -> List[FloorSheet]:
        """Returns the floorsheet data for the current date

        Returns:
            List[FloorSheet]: List of floorsheet data in form of `FloorSheet`
        """
        contents = []
        tasks = []

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
            await asyncio.sleep(2)

        for page_no in range(pages):
            tasks.append(_get_floorsheet_page(page_no))

        await asyncio.gather(*tasks)
        return contents
