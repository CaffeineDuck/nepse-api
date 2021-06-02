from dataclasses import asdict

import httpx
import humps
import pytest

from nepse import Client
from nepse.utils import ClientWrapperHTTPX


@pytest.mark.asyncio
async def test_right_security_data():
    session = httpx.AsyncClient()
    wrapper_client = ClientWrapperHTTPX(session)
    data = await wrapper_client.get_json(
        "https://newweb.nepalstock.com/api/nots/security/2792"
    )
    api_data = humps.decamelize(data)
    await session.aclose()

    nepse_client = Client(True, 10)
    wrapper_data = asdict(
        await nepse_client.security_client.get_company(symbol="UPPER")
    )
    await nepse_client.close()

    assert api_data == wrapper_data
