from enum import Enum
from datetime import date
from httpx import Response

from schwabpy_api.schwab.enums import (
    Quote,
    Option,
    Markets,
)
from schwabpy_api.schwab.utils import (
    CustomCRUD,
    validate_enums_iterable,
    check_enum_value,
    is_ticker_fmt_valid,
)

MARKET_DATA_PATH = "/marketdata/v1"
ACCOUNT_TRADER_PATH = "/trader/v1"


class Quotes:
    def __init__(self, client: CustomCRUD):
        self.client = client

    async def get_quote(self, ticker: str, fields: list[str | Enum] = None) -> Response:
        """
        Single symbol get quote.

        Args:
            ticker (str)): Publicly listed ticker symbol. Ex. AAPL
            fields (list(str | Enum)): Request subsets of data. By default, none will return all.
        Returns:
            HTTP Response 
        """
        params = {}
        is_ticker_fmt_valid(ticker)
        # TODO: Utility function to check fields in iterable meet
        # enum specification?
        fields = validate_enums_iterable(fields, Quote.Fields)
        if fields:
            params["fields"] = ",".join(fields)

        path = MARKET_DATA_PATH + "/{}/quotes".format(ticker)
        return await self.client._get_request(path, params)

    async def get_quotes(
        self, tickers: list[str], fields: list[str | Enum] = None
    ) -> Response:
        """
        Get quote for a list of symbols.

        Args:
            ticker (list(str)): Comma separated string of symbol(s) to look up ticker symbol.
                Ex. ["AAPL","GOOG"]
            fields (list(str | Enum)): Request subsets of data. By default, none will return all.
        Returns:
            HTTP Response    
        """
        params = {}
        fields = validate_enums_iterable(fields, Quote.Fields)
        if fields:
            params["fields"] = ",".join(fields)

        # TODO: Should catch an error if list entries are not strings?
        if isinstance(tickers, list):
            params["symbols"] = tickers

        path = MARKET_DATA_PATH + "/quotes"
        return await self.client._get_request(path, params)


class Options:
    def __init__(self, client: CustomCRUD):
        self.client = client

    async def get_chain(
        self,
        ticker: str,
        contract_type: str = None,
        range: str = None,
        option_type: str = None,
        expiration_month: str = None,
        strike_count: int = None,
        strike_price: float = None,
        from_date: date = None,
        to_date: date = None,
        volatility: float = None,
        underlying_price: float = None,
        interest_rate: float = None,
        days_to_expiration: int = None,
        strategy: str = Option.Strategy.SINGLE.value,
        interval: float = None,
        entitlement: str = None,
        include_underlying_quote: bool = True,
    ) -> Response:
        """
        Get Option Chain including information on options contracts associated with each expiration.

        Args:
            ticker (str): Publicly listed ticker symbol. Ex. AAPL

        Returns:
            HTTP Response
        """
        params = {}
        if is_ticker_fmt_valid(ticker):
            params["symbol"] = ticker

        params["contractType"] = (
            Option.ContractType.ALL.value
            if contract_type is None
            else check_enum_value(contract_type, Option.ContractType)
        )
        params["range"] = (
            Option.Range.ALL.value
            if range is None
            else check_enum_value(range, Option.Range)
        )
        params["optionType"] = (
            Option.Type.ALL.value
            if option_type is None
            else check_enum_value(option_type, Option.Type)
        )
        params["expMonth"] = (
            Option.ExpirationMonth.ALL.value
            if expiration_month is None
            else check_enum_value(expiration_month, Option.ExpirationMonth)
        )

        if strike_count is not None:
            params["strikeCount"] = strike_count
        if strike_price is not None:
            params["strike"] = strike_price
        if from_date is not None:
            params["fromDate"] = from_date
        if to_date is not None:
            params["toDate"] = to_date
        if volatility is not None:
            params["volatility"] = volatility
        if underlying_price is not None:
            params["underlyingPrice"] = underlying_price
        if interest_rate is not None:
            params["interestRate"] = interest_rate
        if days_to_expiration is not None:
            params["daysToExpiration"] = days_to_expiration
        if strategy is not None:
            params["strategy"] = strategy
        if interval is not None:
            params["interval"] = interval
        if entitlement is not None:
            params["entitlement"] = entitlement
        if include_underlying_quote is not None:
            params["includeUnderlyingQuote"] = include_underlying_quote

        path = MARKET_DATA_PATH + "/chains"
        return await self.client._get_request(path, params)

    async def get_expiration_chain(self, ticker: str) -> Response:
        """
        Get Option Expiration (Series) information for an optionable symbol.
        Does not include individual options contracts for the underlying.

        Args:
            ticker (str): Publicly listed ticker symbol. Ex. AAPL

        Returns:
            HTTP Response            
        """
        params = {}
        if is_ticker_fmt_valid(ticker):
            params["symbol"] = ticker

        path = MARKET_DATA_PATH + "/expirationchain"
        return await self.client._get_request(path, params)


class MarketHours:
    def __init__(self, client: CustomCRUD):
        self.client = client

    # TODO: Currently the Schwab API ONLY support the "equity"
    # market_id endpoint. As such that value is set by default.
    async def get_market_status(
        self, market_id: str = Markets.MktType.EQUITY.value, date: str = None
    ) -> Response:
        """
        Get specific market status. Date will default to today if None provided.

        Args:
            market_id (str): Identification of desired market
            date (str): Desired date in format YYYY-MM-DD
        
        Returns:
            HTTP Response
        """
        params = {}
        if date is not None:
            params["date"] = date
        # Check market id
        market_id = check_enum_value(market_id, Markets.MktType)
        path = MARKET_DATA_PATH + "/markets/{}".format(market_id)
        return await self.client._get_request(path, params)


class UserPreference:
    def __init__(self, client: CustomCRUD):
        self.client = client

    def get_user_preference(
        self,
    ) -> Response:
        """Collect user preferences.

        Returns:
            HTTP Response
        """
        params = {}
        path = ACCOUNT_TRADER_PATH + "/userPreference"
        return self.client._get_request(path, params)
