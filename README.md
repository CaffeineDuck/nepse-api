# NEPSE API Wrapper

This python module fetches the data from [Nepali Stock Site](https://newweb.nepalstock.com/) and provides them in a pythonic
and usable way.


## About

This is a API wrapper for NEPSE API. This project was inspired from [PyPi Nepse](https://github.com/pyFrappe/nepse). 

## How to use?

You can use this by package from [Nepse API PyPi](https://pypi.org/project/nepse-api/)
```sh
pip install nepse-api
```

## Why use this?

How is this better than [PyPi Nepse](https://github.com/pyFrappe/nepse)?
- It is asynchronous.
- Data can be taken as attributes rather than from dict.
- Data is fetched from the API rather than scraping the site.
- Data is cached 

## APIs used

The APIs that I used to create this API wrapper is:
- https://newweb.nepalstock.com/api/

## How to use?

```py
import asyncio
import httpx
from nepse import Client

async def main():

    # Doing this is optional you can directly
    # Initialize using `client = Client()` as well
    async with httpx.AsyncClient() as async_client:
        # Initializes the client
        client = Client(httpx_client=async_client)

        # Gets the data
        data = await client.security_client.get_company(symbol="UPPER")

        # Prints the highest price for that company today
        print(data.security_daily_trade_dto.high_price)
    
# Run the function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Why are the attributes so in-costistent?

The attribues are in-consistent because the attributes are set according to the response set by the API. I tried changing 
it up but that would be distruptive because the comability with the API would be broken. 

## Documentation?

Documentation is still in progress!

## Want To Contribute?

You can send a pull request or open an issue to contribute.