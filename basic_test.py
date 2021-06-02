import asyncio
from dataclasses import asdict
from textwrap import wrap

import httpx
import humps
import pytest

from nepse import Client
from nepse.security.types import BaseSecurity
from nepse.utils import ClientWrapperHTTPX


@pytest.mark.asyncio
async def test_all_companies():
    async with httpx.AsyncClient() as async_client:
        nepse_client = Client(httpx_client=async_client)
        api_data = await nepse_client.security_client.get_companies()
        assert api_data


@pytest.mark.asyncio
async def test_right_security_data():
    async with httpx.AsyncClient() as async_client:
        wrapper_client = ClientWrapperHTTPX(async_client)
        data = await wrapper_client.get_json(
            "https://newweb.nepalstock.com/api/nots/security/2792"
        )
        api_data = humps.decamelize(data)

    async with httpx.AsyncClient() as async_client:
        nepse_client = Client(httpx_client=async_client)
        wrapper_data = asdict(
            await nepse_client.security_client.get_company(symbol="UPPER")
        )

    assert api_data == wrapper_data
