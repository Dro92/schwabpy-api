from enum import Enum


class Token(Enum):
    EXPIRES_IN: str = "expires_in"
    EXPIRES_AT: str = "expires_at"
    REFRESH_TOKEN: str = "refresh_token"
    ACESS_TOKEN: str = "access_token"


class Quote:
    class Fields(Enum):
        QUOTE: str = "quote"
        FUNDAMENTAL: str = "fundamental"
        EXTENDED: str = "extended"
        REFERENCE: str = "reference"
        REGULAR: str = "regular"


class Markets:
    class MktType(Enum):
        BOND: str = "bond"
        EQUITY: str = "equity"
        OPTION: str = "option"
        FUTURE: str = "future"
        FOREX: str = "forex"

    class Session(Enum):
        PRE_MARKET: str = "preMarket"
        REG_MARKET: str = "regularMarket"
        POST_MARKET: str = "postMarket"


class Option:
    class ContractType(Enum):
        ALL = "ALL"
        CALL = "CALL"
        PUT = "PUT"

    class Range(Enum):
        ALL = "ALL"
        IN_THE_MONEY = "ITM"
        NEAR_THE_MONEY = "NTM"
        OUT_OF_THE_MONEY = "OTM"
        STRIKE_ABOVE_MARKET = "SAK"
        STRIKE_NEAR_MARKET = "SNK"
        STRIKE_BELOW_MARKET = "SBK"

    class Type(Enum):
        ALL = "ALL"
        STANDARD = "S"
        NON_STANDARD = "NS"

    class ExpirationMonth(Enum):
        ALL = "ALL"
        JANUARY = "JAN"
        FEBRUARY = "FEB"
        MARCH = "MAR"
        APRIL = "APR"
        MAY = "MAY"
        JUNE = "JUN"
        JULY = "JUL"
        AUGUST = "AUG"
        SEPTEMBER = "SEP"
        OCTOBER = "OCT"
        NOVEMBER = "NOV"
        DECEMBER = "DEC"

    class Entitlement(Enum):
        PAYING_PRO = "PP"
        NON_PAYING_PRO = "PN"
        NON_PRO = "NP"

    class Strategy(Enum):
        SINGLE = "SINGLE"
        ANALYTICAL = "ANALYTICAL"
        COVERED = "COVERED"
        VERTICAL = "VERTICAL"
        CONDOR = "CONDOR"
        DIAGONAL = "DIAGONAL"
        ROLL = "ROLL"
        CALENDAR = "CALENDAR"
        COLLAR = "COLLAR"
        STRANGLE = "STRANGLE"
        STRADDLE = "STRADDLE"
        BUTTERFLY = "BUTTERFLY"


class Streamer:
    class Command(Enum):
        LOGIN = "LOGIN"
        SUBS = "SUBS"
        ADD = "ADD"
        UNSUBS = "UNSUBS"
        VIEW = "VIEW"
        LOGOUT = "LOGOUT"

    class ServiceName(Enum):
        ADMIN = "ADMIN"
        LEVELONE_EQUITY = "LEVELONE_EQUITIES"
        LEVELONE_OPTIONS = "LEVELONE_OPTIONS"
        BOOK = "BOOK"

    class BookService(Enum):
        NYSE_BOOK = "NYSE_BOOK"
        NASDAQ_BOOK = "NASDAQ_BOOK"
        OPTIONS_BOOK = "OPTIONS_BOOK"
