from httpx import Response
import httpx
from enum import EnumMeta, Enum
from collections.abc import Iterable
from datetime import datetime, timezone
import json
from abc import ABC, abstractmethod
from authlib.integrations.base_client.errors import InvalidTokenError
import asyncio
from typing import Union

from websockets.legacy import client as ws_client
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedOK,
    ConnectionClosedError,
)

from schwabpy_api.utils.log import logger
from schwabpy_api.schwab.auth import SchwabAsyncOAuth

SCHWAB_API_ROOT_DOMAIN = "https://api.schwabapi.com"


def check_enum_value(field: str | Enum, enum_cls: EnumMeta) -> str:
    """Helper to return the enum value based on string or enum member.

    :param iterable: Either a string or Enum member
    :type iterable: str or Enum
    :param enum_cls: Enum class to validate against
    :type enum_cls: Enum
    """
    # If the field is an Enum member
    if isinstance(field, enum_cls):
        return field.value
    elif isinstance(field, str):
        valid_value = {member.value for member in enum_cls}
        # Check if valid member name
        if field in valid_value:
            return field
        else:
            raise ValueError(
                f"""{field} is not a valid member of {enum_cls}.
                Re-attempt using one of these {valid_value}.
                """
            )
    else:
        raise ValueError(f"{field} is neither a string nor valid {enum_cls} member.")


def validate_enums_iterable(iterable: list, enum_cls: EnumMeta) -> list:
    """
    Helper to valide provided values are part of an enum class. Accepts
    both string names or Enum members.

    :param iterable: A lit of either strings or Enum members
    :type iterable: list
    :param enum_cls: Enum class to validate against
    :type enum_cls: Enum
    """

    if iterable is None:
        return []
    if not isinstance(enum_cls, EnumMeta):
        raise ValueError(f"Provided {enum_cls} class is not type Enum.")

    if isinstance(iterable, Iterable):
        return [check_enum_value(val, enum_cls) for val in iterable]
    return [check_enum_value(iterable, enum_cls)]


def is_ticker_fmt_valid(ticker: str) -> bool:
    """Check if a ticker symbol is all caps. If not raise a ValueError.

    :param ticker: Company publicly listed ticker symbol.
    :type ticker: str
    :return: bool
    """
    if not ticker.isupper():
        raise ValueError(f"{ticker} is not the proper ALL CAPS format.")
    return True


def is_date_fmt_valid(date: str) -> bool:
    """Check if date string is in the format YYYY-MM-DD

    :param date: Date in format YYYY-MM-DD
    :type date: str
    :return: bool
    """
    if not datetime.strptime(date, "%Y-%m-d"):
        raise ValueError(f"{date} is not in the format YYYY-MM-DD")
    return True


def convert_list_to_csv_string(input: list[str]) -> str:
    """Convert a list to a comma separated string.

    :param input: List of strings
    :type input: List of strings
    :return: str
    """
    return ",".join(input)


def parse_option_string(input: str) -> str:
    """
    Converts "AAPL241115C00200" to
    "AAPL  241115C00200000"
    """
    i = 0
    # Loop over string characters until first number
    while i < len(input) and not input[i].isdigit():
        i += 1
    # Left adjust symbol and right pad with spaces as needed
    symbol_root = input[:i].ljust(6)
    date_str = input[i : i + 6]  # Extract YYMMDD segment
    option_type = input[i + 6]  # Extract option type ('C' or 'P)
    # Left adjust strike price and pad significant digits with 0 as needed
    strike_price = input[i + 7 :].ljust(8, "0")
    # Schwab expected format
    output = f"{symbol_root}{date_str}{option_type}{strike_price}"
    return output


def check_mkt_hours(otime: str, ctime: str) -> bool:
    """
    Check if the market is open at this time.
    :type open: str
    :param open: ISO formatted datetime string
    :type close: str
    :param close: ISO formatted datetime string
    :return: bool
    """

    open_time = datetime.fromisoformat(otime).astimezone(timezone.utc)
    close_time = datetime.fromisoformat(ctime).astimezone(timezone.utc)
    # Get current market local time
    # eastern = pytz.timezone("America/New_York")
    current_time = datetime.now(timezone.utc)
    logger.info(f"Current time: {current_time} Close time: {close_time}")
    return True if open_time < current_time < close_time else False


class CustomCRUD:
    """ """

    def __init__(
        self,
        session: SchwabAsyncOAuth,
        timeout: float = 10.0,
    ):
        self.session = session
        self.token_info = session.token
        self.set_timeout(timeout)  # Set default timeout

    def _check_response(self, response: Response) -> Response:
        """
        Helper to verify response status and return dict
        if successful.

        :type response: Response
        :param response: HTTP Response to verify and process
        """
        try:
            response.raise_for_status()
            return response
        except (httpx.HTTPStatusError, httpx.HTTPError) as e:
            logger.exception("HTTP Error", exc_info=e)
        except Exception as e:
            logger.exception("Unexpected error", exc_info=e)

    # Define custom CRUD to modify URL path based on desired function
    async def _get_request(self, path: str, data: dict) -> dict:
        url = SCHWAB_API_ROOT_DOMAIN + path
        # TODO: Add some logging to debug? Need to protect sensitive data

        # Handle token refresh
        try:
            resp = await self.session.get(url=url, params=data)
            return self._check_response(resp)
        except InvalidTokenError:
            await self.session.check_authentication()

    async def _post_request(self, path: str, data: dict) -> dict:
        url = SCHWAB_API_ROOT_DOMAIN + path
        # TODO: Add some logging to debug? Need to protect sensitive data

        # Handle token refresh
        try:
            resp = await self.session.post(url=url, json=data)
            return self._check_response(resp)
        except InvalidTokenError:
            await self.session.check_authentication()

    async def _put_request(self, path: str, data: dict) -> dict:
        url = SCHWAB_API_ROOT_DOMAIN + path
        # TODO: Add some logging to debug? Need to protect sensitive data

        # Handle token refresh
        try:
            resp = await self.session.put(url=url, json=data)
            return self._check_response(resp)
        except InvalidTokenError:
            await self.session.check_authentication()

    async def _delete_request(self, path: str, data: dict) -> dict:
        url = SCHWAB_API_ROOT_DOMAIN + path
        # TODO: Add some logging to debug? Need to protect sensitive data

        # Handle token refresh
        try:
            resp = await self.session.delete(url=url, params=data)
            return self._check_response(resp)
        except InvalidTokenError:
            await self.session.check_authentication()

    def set_timeout(self, timeout: float) -> None:
        """Sets the timeout configuration for all HTTP calls. Refer to
        https://www.python-httpx.org/advanced/timeouts/ for specifics.

        :param timeout: Timeout for http requests.
        :type timeout: float
        """
        self.session.timeout = timeout


class CustomSocket(ABC):
    def __init__(self):
        self._stream_customer_id = None
        self._stream_correl_id = None
        # Request attributes
        self._request_id = 0
        self._lock = asyncio.Lock()
        self.send_queue = asyncio.Queue()
        self.receive_queue = asyncio.Queue()
        self._ws = ws_client.WebSocketClientProtocol
        self._timeout = 2  # Timeout for empty queues

    @abstractmethod
    async def connect(
        self,
    ):
        """User to implement custom connection."""
        pass

    async def _send_msg(self) -> None:
        """Send message to socket client from queue."""
        while True:
            if self._ws.closed or self._ws is None:
                # If connection is closed skip processing queue.
                logger.debug("Connection is closed. Try re-connecting.")
                await asyncio.sleep(1.0)
                continue
            try:
                # Get message from queue without blocking if there is none
                msg_to_send = await asyncio.wait_for(
                    self.send_queue.get(), timeout=self._timeout
                )
                # Send the message via socket client
                await self._ws.send(msg_to_send)
                self.send_queue.task_done()
                # logger.debug("Sending message", extra=msg_to_send)
            except asyncio.TimeoutError:
                # logger.debug("Send Queue empty. AsyncIO timeout.")
                # If queue is empty, wait briefly before re-checking
                # await asyncio.sleep(1.0)
                continue
            except asyncio.QueueEmpty:
                logger.debug("Queue is empty.")
            except (ConnectionClosed, ConnectionClosedOK, ConnectionClosedError) as e:
                logger.debug("Socket error", exc_info=e)
                # TODO: Any reconnection logic needed?

    async def _recv_msg(self) -> None:
        """Receive from socket client and place into queue."""
        while True:
            if self._ws.closed or self._ws is None:
                logger.debug("Connection is closed. Try re-connecting.")
                await asyncio.sleep(1.0)
                continue
            try:
                msg = await asyncio.wait_for(self._ws.recv(), timeout=self._timeout)
                # TODO: Logging at receiving, before placing in queue bad?
                # logger.debug("Received message", extra=json.dumps(msg))
                await self.receive_queue.put(msg)
            except asyncio.TimeoutError:
                # logger.debug("Receive Queue empty. AsyncIO timeout.")
                # If queue is empty, wait briefly before re-checking
                # await asyncio.sleep(1.0)
                continue
            except (ConnectionClosed, ConnectionClosedError) as e:
                logger.debug("Connection closed error", exc_info=e)
                # TODO: Any reconnection logic needed?
            except Exception as e:
                logger.exception("Unexpected error", exc_info=e)

    async def produce(self, request: dict):
        """Put message into the send queue."""
        # TODO: Any serialization error handling here?
        await self.send_queue.put(json.dumps(request))

    async def consume(self) -> dict:
        """Consume message from the receive queue."""
        msg_str: Union[str, bytes] = await self.receive_queue.get()
        try:
            return json.loads(msg_str)
        except asyncio.QueueEmpty:
            logger.debug("Queue is empty.")
        except json.JSONDecodeError as e:
            logger.exception("Consume failed.", exc_info=e)
        finally:
            self.receive_queue.task_done()
