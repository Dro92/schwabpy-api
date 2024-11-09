from websockets import client as ws_client

import asyncio

from schwabpy_api.schwab.auth import SchwabAsyncOAuth
from schwabpy_api.schwab.enums import Streamer
from schwabpy_api.schwab.services import (
    LevelOneEquities,
    LevelOneOptions,
    Book,
)
from schwabpy_api.schwab.utils import (
    CustomSocket,
)

from schwabpy_api.utils.log import logger


class StreamClient(CustomSocket):
    def __init__(self, session: SchwabAsyncOAuth, user_preference: dict):
        super().__init__()
        self.client = session
        self.user_preference = user_preference
        # Configured upon login
        self._account = None
        self._stream_customer_id = None
        self._stream_correl_id = None
        self._stream_channel = None
        self._stream_function_id = None
        self._stream_socket_url = None
        # Request attributes
        self._url = None

    async def _is_login_success(self) -> bool:
        """Check login response status.

        :return: bool
        """
        login_response = {}
        while not login_response:
            login_response = await self.consume()
            if not login_response:
                await asyncio.sleep(0.1)
        try:
            status_code = login_response["response"][0]["content"]["code"]
            status = True if status_code == 0 else False
            return status
        except KeyError:
            # TODO:Let user handle error?
            pass

    def _init_login_params(self) -> dict:
        """Initialize login parameters for stream channel."""
        # response = self.user_preference
        # # if response.status_code is not httpx.codes.OK:
        # #     response.raise_for_status()  # Raises HTTPStatusError

        # data = response.json()  # Extract response data
        data = self.user_preference
        try:
            stream_info = data["streamerInfo"][0]
            self._stream_customer_id = stream_info["schwabClientCustomerId"]
            self._stream_channel = stream_info["schwabClientChannel"]
            self._stream_correl_id = stream_info["schwabClientCorrelId"]
            self._stream_function_id = stream_info["schwabClientFunctionId"]
            self._stream_socket_url = stream_info["streamerSocketUrl"]
        except KeyError as e:
            logger.debug("KeyError accessing user preferences params.", extra=e)
        return {
            "Authorization": self.client.token["access_token"],
            "SchwabClientChannel": self._stream_channel,
            "SchwabClientFunctionId": self._stream_function_id,
        }

    def request_format(
        self,
        service: str,
        command: str,
        params: dict,
    ) -> dict:
        """Format requests to meet Schwab field requirements."""
        request_id = self._request_id
        self._request_id += 1  # Increment id count
        return {
            "service": service,
            "requestid": str(request_id),
            "command": command,
            "SchwabClientCustomerId": self._stream_customer_id,
            "SchwabClientCorrelId": self._stream_correl_id,
            "parameters": params,
        }

    async def subscribe_service(
        self,
        service_dict: dict,
    ):
        request_id = self._request_id
        self._request_id += 1  # Increment id count
        request = {
            "service": service_dict["service"],
            "requestid": str(request_id),
            "command": service_dict["command"],
            "SchwabClientCustomerId": self._stream_customer_id,
            "SchwabClientCorrelId": self._stream_correl_id,
            "parameters": service_dict["parameters"],
        }
        requests = {"requests": [request]}
        await self.produce(requests)

    # Login
    async def connect(self, ws_conn_args=None) -> None:
        # Initialize login parameters for stream channel
        login_request_params = self._init_login_params()

        login_request = self.request_format(
            service=Streamer.ServiceName.ADMIN.value,
            command=Streamer.Command.LOGIN.value,
            params=login_request_params,
        )
        # async with ws_client.connect(self._stream_socket_url) as ws:
        self._ws = await ws_client.connect(self._stream_socket_url)

        # Create coroutine sender and receiver tasks
        asyncio.create_task(self._recv_msg())
        asyncio.create_task(self._send_msg())

        # Send initial login message to establish socket connection
        await self.produce(login_request)

        # Verify login response
        if not await self._is_login_success():
            # TODO: Raise InvalidHandshake error?
            logger.debug("LOGIN FAILED.")
        logger.debug("LOGIN SUCCESS.")

    async def level_one_equities_sub(
        self, tickers: list[str], fields: list[str] = None
    ) -> dict:
        data = LevelOneEquities.level_one_equities_sub(tickers, fields)
        await self.subscribe_service(data)

    async def level_one_options_sub(
        self, tickers: list[str], fields: list[str] = None
    ) -> dict:
        """
        Subcribe to a stream for specific options contracts.

        :type tickers: list[str]
        :param tickers: Comma separated value of options symbols must
        follow the format "RRRRRRYYMMDDsWWWWWddd".

                RRRRRR denotes the ticker symbol.

                YYMMDD denotes year, month and day.

                s denotes contract type Call (C) or Put (P).

                WWWWW denotes the strike price I.E. 00225 for 225

                ddd denotes decimal precision.
        """
        data = LevelOneOptions.level_one_options_sub(tickers, fields)
        await self.subscribe_service(data)

    async def options_book(
        self,
        tickers: list[str],
        fields: list[str] = None,
    ) -> dict:
        """
        Subcribe to a stream for specific options contracts.

        :type tickers: list[str]
        :param tickers: Comma separated value of options symbols must
        follow the format "RRRRRRYYMMDDsWWWWWddd".

                RRRRRR denotes the ticker symbol.

                YYMMDD denotes year, month and day.

                s denotes contract type Call (C) or Put (P).

                WWWWW denotes the strike price I.E. 00225 for 225

                ddd denotes decimal precision.
        """
        data = Book.options_book(tickers, fields)
        await self.subscribe_service(data)

    async def nasdaq_book(
        self,
        tickers: list[str],
        fields: list[str] = None,
    ) -> dict:
        data = Book.nasdaq_book(tickers, fields)
        await self.subscribe_service(data)
