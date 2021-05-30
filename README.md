# NEPSE API Wrapper

This python module fetches the data from [Nepali Stock Site](https://newweb.nepalstock.com/) and provides them in a pythonic
and usable way.


## About

This is a API wrapper for NEPSE API. This project was inspired from [PyPi Nepse](https://github.com/pyFrappe/nepse). 

## Why use this?

How is this better than [PyPi Nepse](https://github.com/pyFrappe/nepse)?
- It is asynchronous.
- Data can be taken as attributes rather than from dict.
- Data is fetched from the API rather than scraping the site.
- Data is cached 

## APIs used

The APIs that I used to create this API wrapper is:
- https://newweb.nepalstock.com/api/nots/security/

## How to use?

```py
import asyncio
from nepse import Client

async def main():
    # Initializes the client
    client = Client()

    # Gets the data
    data = await client.get_company(symbol="UPPER")

    # Prints the highest price for that company today
    print(data.daily_trade.high_price)

    # Properly closes the session
    await client.close()
    
# Run the function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Documentation?

Documentation is still in progress!

## Want To Contribute?

You can send a pull request or open an issue to contribute.