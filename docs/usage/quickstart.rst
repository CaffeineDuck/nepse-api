.. _quickstart:

.. currentmodule:: nepse

Quickstart
============

This page gives a brief introduction to the library. It assumes you have the library installed,
if you don't check the :ref:`installing` portion.

Let's get today's highest price of **Upper Tamakoshi Hydropower Ltd**
It looks something like this:

.. code-block:: python
    :linenos:
    
    import asyncio
    import httpx
    from nepse import Client

    async def main():

        # Initializes the client
        client = Client()

        # Gets the data
        data = await client.security_client.get_company(symbol="UPPER")

        # Prints the highest price for that company today
        print(data.high_price)

        # Closes the session
        await client.close()
        
    # Run the function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Let's name this file ``nepse_upper.py``. Make sure to not name it ``nepse.py`` as that'll conflict
with the library

There is not a log going on here. So lets walk you through step by step.

1. The first line just imports the library and other dependencies, if this raises a `ModuleNotFoundError` or `ImportError`
   then head on over to :ref:`installing` section to properly install.

2. Next, we create an instance of a :class:`Client`. This client is the way through which we interact with the NEPSE API.

3. Now, we get the company with symbol *UPPER*.

4. We print its highest price for today.

5. We close the client for cleaning up.

6. We get the event_loop using asyncio and run the async function in that event_loop.

On Windows:

.. code-block:: shell

    $ py -3 nepse_upper.py

On other systems:

.. code-block:: shell

    $ python3 nepse_upper.py