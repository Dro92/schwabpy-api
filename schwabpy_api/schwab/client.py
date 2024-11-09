from datetime import datetime, timezone
from trader.schwab.auth import SchwabAsyncOAuth
from trader.schwab.utils import (
    CustomCRUD,
    check_enum_value,
    check_mkt_hours,
)
from trader.schwab.endpoints import (
    Quotes,
    Options,
    MarketHours,
    UserPreference,
)

from trader.schwab.enums import (
    Markets,
)

# From Schwab docs
TOKEN_OAUTH_ENDPOINT = "https://api.schwabapi.com/v1/oauth/token"
AUTHORIZATION_URL_BASE = "https://api.schwabapi.com/v1/oauth/authorize"


class SchwabClient:
    """
    Schwab Client which handles

    Attributes:
        client_id (str): Schwab developer client string.
        
        auth_session (SchwabAsyncOAuth): Async OAuth Session
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        callback_uri: str,
        token_url: str = TOKEN_OAUTH_ENDPOINT,
        auth_url: str = AUTHORIZATION_URL_BASE,
        timeout: float = 10.0,
    ):
        """
        Initializes a Schwab client interface.

        Args:
            client_id (str): Schwab developer client string.
        """
        # TODO: Should the session have some built in token management or
        # should the client access token_info to allow user control over how
        # it gets refreshed/manipulated?
        self.auth_session = SchwabAsyncOAuth(
            client_id=client_id,
            client_secret=client_secret,
            callback_uri=callback_uri,
            token_url=token_url,
            auth_url=auth_url,
        )
        # Instantiate custom CRUD
        self._crud = CustomCRUD(self.auth_session, timeout)
        # Market data
        self.quotes = Quotes(self._crud)
        self.options = Options(self._crud)
        self.market_status = MarketHours(self._crud)

        # Account info. and trades
        self.user_preference = UserPreference(self._crud)

    async def is_market_open(
        self,
        mkt_session: str = None,
        date: str = None,
    ) -> dict:
        """
        
        Args:
            mkt_session (str): Market session hours to use.
            date (str): Desired date in format YYYY-MM-DD
            
        Returns:
            dict: Market status.
        """
        response = await self.market_status.get_market_status(date=date)
        # TODO: Currently the Schwab API has very brittle behavior. When the
        # market is closed that day, it changes the second key to "equity".
        # When open, it uses "EQ". The "isOpen" key does not update with time
        # rather it only indicates if the market is open THAT day. Assume this
        # will be fixed some day and support both conditions for now.
        # Market is closed today response
        response = response.json()
        if "equity" in response["equity"]:
            path = response["equity"]["equity"]
        # Market is open today response
        elif "EQ" in response["equity"]:
            path = response["equity"]["EQ"]

        # TODO: This is redundant and could be done earlier, but for now
        # assume Schwab will eventually fix the API.
        mkt_open_today = path["isOpen"]

        # TODO: Setup a response dict withs status and times
        mkt_status = {
            "status": None,
            "openTime": None,
            "closeTime": None
        }
        if not mkt_open_today:
            return mkt_status

        # Check market session
        mkt_session = (
            check_enum_value(mkt_session, Markets.Session)
            if mkt_session is not None
            else Markets.Session.REG_MARKET.value
        )
        session_hours = "sessionHours"
        otime = path[session_hours][mkt_session][0]["start"]
        ctime = path[session_hours][mkt_session][0]["end"]
        # Convert to Zulu time
        mkt_status["openTime"] = datetime.fromisoformat(
            otime).astimezone(timezone.utc)
        mkt_status["closeTime"] = datetime.fromisoformat(
            ctime).astimezone(timezone.utc)
        mkt_status["status"] = check_mkt_hours(otime, ctime)
        return mkt_status