from typing import List

import humps

from nepse.market.types import MarketCap
from nepse.utils import _ClientWrapperHTTPX

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
