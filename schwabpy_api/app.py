import asyncio
import os

from schwabpy_api.schwab.client import SchwabClient
from schwabpy_api.utils.log import logger
from schwabpy_api.processing.options_processing import (
    concatenate_option_map,
    process_option_chain_response,
    OptionChain
)
from schwabpy_api.processing.quote_processing import process_equity_response, EquityResponse
from schwabpy_api.utils.util import measure_response_time, iso_time_now
from schwabpy_api.utils.loghelper import LoggingDescriptor, LogOptionsMetrics, LogEquitiesMetrics

# Database
from schwabpy_api.database.db_manager import InfluxDBHandler
from datetime import datetime, timezone

# Import environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DB_HOST = os.getenv("DB_HOST")
DB_TOKEN = os.getenv("DB_TOKEN")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false")



async def update_market_times(
    sc: SchwabClient,
    mkt_status: dict,
    mkt_session: str = None,
    interval: int = 3600
) -> None:
    """
    Routinely check the status of the market and set
    the shared variable.

    Args:
        sc (SchwabClient): Schwab asynchronous HTTP client
        interval (int): Period to check market status
        mkt_session (str): Pre-market, regular or after hours.
    """
    while True:
        try:
            # Delay how often this loop runs
            await asyncio.sleep(interval)
            # Request status
            updated_status = await sc.is_market_open(mkt_session)
            okey = "openTime"
            ckey = "closeTime"
            # Update shared dict
            mkt_status[okey] = updated_status[okey]
            mkt_status[ckey] =  updated_status[ckey]
            logger.info("Requested market status.", extra=mkt_status)
        except Exception as e:
            logger.exception("Failed market status check.", exc_info=e)

async def market_status_interrupt(
    mkt_status: dict,
    mkt_interrupt: asyncio.Event,
) -> None:
    """
    Routinely check the status of the market and set
    the global variable.

    Args:
        sc (SchwabClient): Schwab asynchronous HTTP client
        interval (int): Period to check market status
        mkt_session (str): Pre-market, regular or after hours.
    """
    try:
        while True:
            # UTC time
            now = datetime.now(timezone.utc)
            mkt_open = mkt_status["openTime"] <= now <= mkt_status["closeTime"]
            mkt_interrupt.set() if mkt_open else mkt_interrupt.clear()
            await asyncio.sleep(5)
    except Exception as e:
        logger.exception("Failed market status check.", exc_info=e)

async def request_equity(
    sc: SchwabClient,
    dbc: InfluxDBHandler,
    ticker: str = "SPY"
) -> dict:
    request_time, duration, response = await measure_response_time(
        sc.quotes.get_quote,
        ticker
    )
    data: dict = response.json()
    for _, value in data.items():
        equity = EquityResponse()
        equity_cls = equity.from_dict(value)
        await dbc.write_equity(equity_cls, request_time)
        data[ticker] = equity_cls.to_dict()
        metrics = LogEquitiesMetrics(request_time, data, duration).to_dict()
        await dbc.Write_equity_metrics(metrics, request_time)
        logger.info(f"{LoggingDescriptor.EQUITY_QUOTE.value}", extra=metrics)
    return data

async def request_option_chain(
    sc: SchwabClient,
    dbc: InfluxDBHandler,
    ticker: str = "SPY"
) -> OptionChain:
    """
    Implements an asynchronous gather of the CALL and PUT options chain.
    This is a better implementation as long chains can be impacted by
    networking side delays.
    
    """
    call_type = "CALL"
    put_type = "PUT"
    request_time = iso_time_now()
    # TODO: Define exception handling for asyncio.gather?
    call_response, put_response = await asyncio.gather(
        sc.options.get_chain(ticker, contract_type=call_type),
        sc.options.get_chain(ticker, contract_type=put_type)
    )
    option_chain = concatenate_option_map(call_response, put_response)
    response_time = max(
        call_response.elapsed.total_seconds(),
        put_response.elapsed.total_seconds()
    )
    await dbc.write_options(
        data=option_chain.to_dict(),
        time_now=request_time
    )
    metrics = LogOptionsMetrics(request_time, option_chain, response_time).to_dict()
    await dbc.write_option_metrics(metrics, request_time)
    logger.info(f"{LoggingDescriptor.OPTION_QUOTE.value}", extra=metrics)
    return option_chain

async def market_function(
    sc: SchwabClient,
    dbc: InfluxDBHandler,
    mkt_interrupt: asyncio.Event
) -> None:
    """
    User defined functionality would go in here.

    Args:
        sc (SchwabClient): Schwab asynchronous HTTP client
    """
    await mkt_interrupt.wait()  # Wait for market to be open
    poll_interval = 3
    ticker = "SPY"
    while True:
        try:
            asyncio.gather(
                request_equity(sc, dbc, ticker),
                request_option_chain(sc, dbc, ticker)
            )
            await asyncio.sleep(poll_interval)
        except Exception as e:
            logger.exception("Exc occurred.", exc_info=e)

async def main():
    # Instantiate Schwab client
    sc = SchwabClient(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, callback_uri=REDIRECT_URI
    )
    # Check authentication token status
    await sc.auth_session.check_authentication()
  
    # Instantiate database handler
    dbc = InfluxDBHandler(
        host=DB_HOST,
        token=DB_TOKEN,
        org="influxdata",
        bucket="default"
    )
    # Connect to database
    await dbc.connect()

    # Set market interrupt lock and initialize to false
    mkt_interrupt = asyncio.Event()

    # Initialize shared times dict
    mkt_status = await sc.is_market_open()

    # Debug dict only
    # mkt_status = {
    #     "status": True,
    #     "openTime": datetime.fromisoformat("2024-10-27T19:00:26.520800+00:00").astimezone(timezone.utc),
    #     "closeTime": datetime.fromisoformat("2024-10-27T20:10:00.520800+00:00").astimezone(timezone.utc)
    # }

    # Start market time update task
    asyncio.create_task(update_market_times(sc, mkt_status))

    # Start market status inerrupt task
    asyncio.create_task(market_status_interrupt(
        mkt_status, 
        mkt_interrupt
    ))

    await market_function(sc, dbc, mkt_interrupt)


if __name__ == "__main__":
    logger.setLevel(LOG_LEVEL)

    if CLIENT_ID is None:
        raise ValueError("'CLIENT_ID' not defined.")
    elif CLIENT_SECRET is None:
        raise ValueError("'CLIENT_SECRET' not defined.")
    elif REDIRECT_URI is None:
        raise ValueError("'REDIRECT_URI' not defined.")

    asyncio.run(main())
