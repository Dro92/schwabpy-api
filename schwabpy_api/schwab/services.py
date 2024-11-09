from enum import Enum

from schwabpy_api.schwab.enums import Streamer
from schwabpy_api.schwab.utils import (
    parse_option_string,
    convert_list_to_csv_string,
)


class LevelOneEquities:
    class Fields(Enum):
        DEFAULT = 0  # Default MUST include: place holder for ticker
        BID_PRICE = 1  # Bid price
        ASK_PRICE = 2  # Ask price
        LAST_PRICE = 3  # Last price
        BID_SIZE = 4  # Size of the highest bid
        ASK_SIZE = 5  # Size of the lowest ask
        ASK_ID = 6  # Exchange ID of the lowest ask
        BID_ID = 7  # Exchange ID of the highest bid
        TOTAL_VOLUME = 8  # Total volume trade to date
        LAST_SIZE = 9  # Size of the last trade
        HIGH_PRICE = 10  # Daily high price
        LOW_PRICE = 11  # Daily low price
        CLOSE_PRICE = 12  # Previous close price
        EXCHANGE_ID = 13  # Exchange ID
        MARGINABLE = 14  # Is this equity marginable?
        DESCRIPTION = 15  # Description
        LAST_ID = 16  # Exchange ID of the last trade
        OPEN_PRICE = 17  # Today's open price
        NET_CHANGE = 18  # Net change
        HIGH_PRICE_52_WEEK = 19  # 52 week high price
        LOW_PRICE_52_WEEK = 20  # 52 week low price
        PE_RATIO = 21  # P/E ratio
        DIVIDEND_AMOUNT = 22  # Dividend amount
        DIVIDEND_YIELD = 23  # Dividend yield
        NAV = 24  # ETF net asset value
        EXCHANGE_NAME = 25  # Exchange name
        DIVIDEND_DATE = 26  # Dividend date
        REGULAR_MARKET_QUOTE = 27  # Regular market quote?
        REGULAR_MARKET_TRADE = 28  # Regular market trade?
        REGULAR_MARKET_LAST_PRICE = 29  # Regular market last price
        REGULAR_MARKET_LAST_SIZE = 30  # Regular market last size
        REGULAR_MARKET_NET_CHANGE = 31  # Regular market net change
        SECURITY_STATUS = 32  # Security status
        MARK = 33  # Mark
        QUOTE_TIME_MILLIS = 34  # Quote time in milliseconds
        TRADE_TIME_MILLIS = 35  # Last trade time in milliseconds
        REGULAR_MARKET_TRADE_MILLIS = 36  # Regular market trade time in milliseconds
        BID_TIME_MILLIS = 37  # Bid time in millis
        ASK_TIME_MILLIS = 38  # Ask time in millis
        ASK_MIC_ID = 39  # Ask Market Identifier Code (MIC)
        BID_MIC_ID = 40  # Bid MIC
        LAST_MIC_ID = 41  # Last trade MIC
        NET_CHANGE_PERCENT = 42  # Net change in percent
        REGULAR_MARKET_CHANGE_PERCENT = 43  # Regular market change in percent
        MARK_CHANGE = 44  # Mark change
        MARK_CHANGE_PERCENT = 45  # Mark change in percent
        HTB_QUANTITY = 46  # HTB quantity
        HTB_RATE = 47  # HTB rate
        HARD_TO_BORROW = 48  # Is this equity hard to borrow?
        IS_SHORTABLE = 49  # Is this equity shortable
        POST_MARKET_NET_CHANGE = 50  # Post market net change
        POST_MARKET_NET_CHANGE_PERCENT = 51  # Post market net change percent
        ALL = (
            "0,1,2,3,4,5,6,7,8,9,"
            "10,11,12,13,14,15,16,17,18,19,"
            "20,21,22,23,24,25,26,27,28,29,"
            "30,31,32,33,34,35,36,37,38,39,"
            "40,41,42,43,44,45,46,47,48,49,"
            "50,51"
        )

    @staticmethod
    def level_one_equities_sub(tickers: list[str], fields: list[str] = None) -> dict:
        fields = (
            LevelOneEquities.Fields.ALL.value
            if fields is None
            else convert_list_to_csv_string(fields)
        )
        params = {"keys": convert_list_to_csv_string(tickers), "fields": fields}
        return {
            "service": Streamer.ServiceName.LEVELONE_EQUITY.value,
            "command": Streamer.Command.SUBS.value,
            "parameters": params,
        }


class LevelOneOptions:
    class Fields(Enum):
        DEFAULT = 0  # Default MUST include: place holder for ticker
        DESCRIPTION = 1  # Description
        BID_PRICE = 2  # Highest bid price
        ASK_PRICE = 3  # Lowest ask price
        LAST_PRICE = 4  # Last trade price
        HIGH_PRICE = 5  # Today's high price
        LOW_PRICE = 6  # Today's low price
        CLOSE_PRICE = 7  # Last close price
        TOTAL_VOLUME = 8  # Today's total volume
        OPEN_INTEREST = 9  # Open interest
        VOLATILITY = 10  # Volatility
        MONEY_INTRINSIC_VALUE = 11  # Money intrinsic value
        EXPIRATION_YEAR = 12  # Expiration year
        MULTIPLIER = 13  # Multiplier
        DIGITS = 14  # Digits
        OPEN_PRICE = 15  # Open price
        BID_SIZE = 16  # Highest bid size
        ASK_SIZE = 17  # Lowest ask size
        LAST_SIZE = 18  # Last trade size
        NET_CHANGE = 19  # Net change
        STRIKE_TYPE = 20  # Strike type
        CONTRACT_TYPE = 21  # Contract type
        UNDERLYING = 22  # Underlying symbol
        EXPIRATION_MONTH = 23  # Expiration month
        DELIVERABLES = 24  # Deliverables
        TIME_VALUE = 25  # Time value
        EXPIRATION_DAY = 26  # Expiration day
        DAYS_TO_EXPIRATION = 27  # Days to expiration
        DELTA = 28  # Delta
        GAMMA = 29  # Gamma
        THETA = 30  # Theta
        VEGA = 31  # Vega
        RHO = 32  # Rho
        SECURITY_STATUS = 33  # Security status
        THEORETICAL_OPTION_VALUE = 34  # Theoretical option value
        UNDERLYING_PRICE = 35  # Underlying price
        UV_EXPIRATION_TYPE = 36  # UV expiration type
        MARK = 37  # Mark
        QUOTE_TIME_MILLIS = 38  # Quote time in millis
        TRADE_TIME_MILLIS = 39  # Last trade time in millis
        EXCHANGE_ID = 40  # Exchange ID
        EXCHANGE_NAME = 41  # Exchange name
        LAST_TRADING_DAY = 42  # Last trading day
        SETTLEMENT_TYPE = 43  # Settlement type
        NET_PERCENT_CHANGE = 44  # Net percent change
        MARK_CHANGE = 45  # Mark change
        MARK_CHANGE_PERCENT = 46  # Mark change in percent
        IMPLIED_YIELD = 47  # Implied yield
        IS_PENNY = 48  # Is penny stock?
        OPTION_ROOT = 49  # Option root
        HIGH_PRICE_52_WEEK = 50  # 52 week high price
        LOW_PRICE_52_WEEK = 51  # 52 week low price
        INDICATIVE_ASKING_PRICE = 52  # Indicative asking price
        INDICATIVE_BID_PRICE = 53  # Indicative bid price
        INDICATIVE_QUOTE_TIME = 54  # Indicative quote time
        EXERCISE_TYPE = 55  # Exercise type
        ALL = (
            "0,1,2,3,4,5,6,7,8,9,"
            "10,11,12,13,14,15,16,17,18,19,"
            "20,21,22,23,24,25,26,27,28,29,"
            "30,31,32,33,34,35,36,37,38,39,"
            "40,41,42,43,44,45,46,47,48,49,"
            "50,51,52,53,54,55"
        )

    @staticmethod
    def level_one_options_sub(tickers: list[str], fields: list[str] = None) -> dict:
        fields = (
            LevelOneOptions.Fields.ALL.value
            if fields is None
            else convert_list_to_csv_string(fields)
        )
        parsed_tickers = [parse_option_string(ticker) for ticker in tickers]
        params = {"keys": convert_list_to_csv_string(parsed_tickers), "fields": fields}
        return {
            "service": Streamer.ServiceName.LEVELONE_OPTIONS.value,
            "command": Streamer.Command.SUBS.value,
            "parameters": params,
        }


class Book:
    class Fields(Enum):
        DEFAULT = 0
        MKT_SNAPSHOT_TIME = 1  # Milliseconds since Epoch
        BID_SIDE_LEVELS = 2  # Price levels
        ASK_SIDE_LEVEL = 3  # Price levels
        ALL = "0,1,2,3"

    class PriceLevels(Enum):
        PRICE = 0  # Price for this level
        AGGREGATE_SIZE = 1  # Aggregate size for this price level
        MKT_MAKER_COUNT = 2  # Number of Market Makers in this price level
        ARRAY_MKT_MAKERS = 3  # Array of market maker sizes for this price level
        ALL = "0,1,2,3"

    class MarketMakers(Enum):
        MKT_MAKER_ID = 0  # Market Maker ID
        SIZE = 1  # Size of the Market Maker for this price level
        QUOTE_TIME = 2  # Quote time in milliseconds for this MM quote
        ALL = "0,1,2"

    @staticmethod
    def options_book(tickers: list[str], fields: list[str] = None) -> dict:
        fields = (
            Book.Fields.ALL.value
            if fields is None
            else convert_list_to_csv_string(fields)
        )
        parsed_tickers = [parse_option_string(ticker) for ticker in tickers]
        params = {"keys": convert_list_to_csv_string(parsed_tickers), "fields": fields}
        return {
            "service": Streamer.BookService.OPTIONS_BOOK.value,
            "command": Streamer.Command.SUBS.value,
            "parameters": params,
        }

    @staticmethod
    def nasdaq_book(tickers: list[str], fields: list[str] = None) -> dict:
        fields = (
            Book.Fields.ALL.value
            if fields is None
            else convert_list_to_csv_string(fields)
        )
        params = {"keys": convert_list_to_csv_string(tickers), "fields": fields}
        return {
            "service": Streamer.BookService.NASDAQ_BOOK.value,
            "command": Streamer.Command.SUBS.value,
            "parameters": params,
        }
