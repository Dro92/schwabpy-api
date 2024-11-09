from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc6749.wrappers import OAuth2Token
import os
from datetime import datetime, timedelta, timezone
import redis
import json

from schwabpy_api.schwab.enums import Token
from schwabpy_api.utils.log import logger

# Schwab token data
# https://developer.schwab.com/products/trader-api--individual/details/documentation/Retail%20Trader%20API%20Production
#
# Access Token:
# To enhance API security, used in place of username+password combination and
# is valid for 30 minutes after creation.

# Bearer Token:
# A Bearer token is the Access Token in the context of an API call for Protected Resource data.
# It is passed in the Authorization header as "Bearer {access_token_value}."

# Refresh Token:
# Renews access to a User's Protected Resources. This may be done before, or at
# any point after the current, valid access_token expires. When they do expire,
# the corresponding Refresh Token is used to request a new Access Token as opposed
# to repeating the entire Flow. This token should be stored for later use and is
# valid for 7 days after creation.
#
# Upon expiration, a new set refresh token must be recreated using the authorization_code Grant Type authentication flow (CAG/LMS).


class TokenManager:
    # TODO: Clean this up later
    TOKEN_KEY = os.getenv("TOKEN_KEY", "schwabToken")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 0)
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

    # def __init__(self, token: dict, timestamp: datetime = None):
    def __init__(self, token: dict = None, timestamp: datetime = None) -> None:
        self.token = token
        # Created timestamp for new tokens
        self.created_timestamp = timestamp or datetime.now(timezone.utc)
        self._key = TokenManager.TOKEN_KEY

    def connect_db(
        self,
    ) -> redis.Redis:
        # TODO: Logic to catch connection issues
        return redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
            password=self.REDIS_PASSWORD,
        )

    @property
    def expires_at(
        self,
    ) -> datetime:
        """
        Returns the tokens `expires_at` value as a datetime object.
        """
        return datetime.fromtimestamp(
            self.token[Token.EXPIRES_AT.value], tz=timezone.utc
        )

    def is_refresh_token_expired(
        self,
    ) -> bool:
        """
        Check if refresh token is valid. Failing this check requires a OAuth2
        process to be re-authenticated by the user.
        """
        return datetime.now(timezone.utc) > (self.created_timestamp + timedelta(days=7))

    def save(
        self,
    ) -> None:
        """
        Save token data to file.
        """
        r = self.connect_db()
        if r is None:
            raise ValueError("No connection to database")
        data = {
            "created_timestamp": self.created_timestamp.timestamp(),
            "token": self.token,
        }
        r.set(self._key, json.dumps(data))

    def load(
        self,
    ) -> None:
        """
        Load token data from file, if it exists, and return ojbect of token.
        If file does not exist return None and handle upstream.
        """
        r = self.connect_db()
        if r is None:
            raise ValueError("No connection to database")
        data = r.get(self._key)
        if data is None:
            raise TypeError(f"Token {self._key} not available")
        # Deserialize JSON
        data = json.loads(data)
        created_timestamp = datetime.fromtimestamp(
            data["created_timestamp"], tz=timezone.utc
        )
        self.token = data["token"]
        self.created_timestamp = created_timestamp


class SchwabAsyncOAuth(AsyncOAuth2Client):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        callback_uri: str,
        auth_url: str,
        token_url: str,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=callback_uri,
        )
        self.auth_url = auth_url
        self.token_url = token_url
        self.token_metadata = TokenManager()  # Contains additional data
        self.token: OAuth2Token = None

    def get_authorization_url(
        self,
        state: str = None,
    ) -> tuple[str, str]:
        """
        Generate authorization code to direct user to Schwab Login Micro Site (LMS)
        """
        auth_uri, state = self.create_authorization_url(self.auth_url, state=state)
        return auth_uri, state

    async def fetch_token(
        self, authorization_response: str, state=None, **kwargs
    ) -> OAuth2Token:
        """
        Obtain response token and metadata.
        """
        self.token = await super().fetch_token(
            url=self.token_url,
            auth=(self.client_id, self.client_secret),
            authorization_response=authorization_response,
        )
        return self.token

    async def manual_authentication(
        self,
    ) -> None:
        # TODO: This is where things will get janky
        # How to somewhat automate this workflow, specifically within headless
        # services? Hosting a web server that then listens on the callback might work.
        #
        # Current process is as follows:
        # 1. Utilize `get_authorization_url()` to generate the necessary URL
        # 2. Navigate to the URL, login to Schwab and authorize
        # 3. Copy callback url from browser and feed it to `fetch_token()`
        #
        # If successful the above will generate a new token which should also be saved.
        # Its refresh token will be valed for <7 days.
        auth_url, state = self.get_authorization_url()
        logger.info(f"Visit URL to authorize: \n{auth_url}\nCurrent state: {state}")

        authorization_response = input("Paste redirect URL here: ")
        logger.info(f"This was received: \n{authorization_response}")

        self.token = await self.fetch_token(authorization_response, state)

        # Update metadata and save new token to file
        self.token_metadata = TokenManager(self.token)
        self.token_metadata.save()

    # TODO: Async authentication can be a problem because the application
    # can attempt to make a request while awaiting authentication to conclude
    # Therefore this operation should be blocking.
    # TODO: Should client check token validity before every request?
    async def check_authentication(
        self,
    ) -> None:
        # TODO: I/O operations are expensive. When calling this method
        # first check if self.token is valid (QUICK). If not, then
        # proceed to load from another location
        if self.token is None or self.token.is_expired():
            try:
                self.token_metadata.load()
            except TypeError:
                await self.manual_authentication()
            except ValueError:
                raise ValueError("Error connecting to database.")

        self.token = self.token_metadata.token
        # Check if the access token is still valid to use
        if not self.token.is_expired():
            return
        # Check if the refresh token is still valid to use
        elif not self.token_metadata.is_refresh_token_expired():
            # Attempt to refresh access token using valid refresh token
            try:
                # Refresh access token
                self.token = await self.refresh_token(
                    self.token_url,
                    refresh_token=self.token_metadata.token[Token.REFRESH_TOKEN.value],
                )
                # Update metadata and save new token
                self.token_metadata.token = self.token
                self.token_metadata.save()
            except Exception as e:
                logger.exception(f"Refreshing access token failed:\n{e}")
                raise
        # Refresh token is no longer valid requiring manual auth
        else:
            await self.manual_authentication()
