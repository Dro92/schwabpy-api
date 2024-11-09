from enum import Enum
from typing import Optional, Dict, Type
from httpx import Response
from schwabpy_api.processing.enums import AssetMainType, AssetSubType


# Enum for ExpirationType
class ExpirationType(Enum):
    M = "M"  # End of Month
    Q = "Q"  # Quarterly
    S = "S"  # 3rd Friday (Regular Options)
    W = "W"  # Weekly (Friday Short Term)


# Enum for SettlementType
class SettlementType(Enum):
    A = "A"  # AM Settlement
    P = "P"  # PM Settlement


# Enum for ExchangeName
class ExchangeName(Enum):
    IND = "IND"
    ASE = "ASE"
    NYS = "NYS"
    NAS = "NAS"
    NAP = "NAP"
    PAC = "PAC"
    OPR = "OPR"
    BATS = "BATS"


class Strategy(Enum):
    SINGLE = "SINGLE"
    ANALYTICAL = "ANALYTICAL"
    COVERED = "COVERED"
    VERTICAL = "VERTICAL"
    CALENDAR = "CALENDAR"
    STRANGLE = "STRANGLE"
    STRADDLE = "STRADDLE"
    BUTTERFLY = "BUTTERFLY"
    CONDOR = "CONDOR"
    DIAGONAL = "DIAGONAL"
    COLLAR = "COLLAR"
    ROLL = "ROLL"


class OptionContractFields(Enum):
    ASK = "ask"  # Current Best Ask Price
    ASK_SIZE = "askSize"  # Number of shares for ask
    BID = "bid"  # Current Best Bid Price
    BID_ASK_SIZE = "bidAskSize"
    BID_SIZE = "bidSize"  # Number of shares for bid
    CLOSE_PRICE = "closePrice"  # Previous day's closing price
    DAYS_TO_EXPIRATION = "daysToExpiration"  # Days to Expiration
    DELIVERABLE_NOTE = "deliverableNote"  # Unit of trade
    DELTA = "delta"  # Delta Value
    DESCRIPTION = "description"  # Description of Instrument
    EXCHANGE_NAME = "exchangeName"  # Exchange Name
    EXERCISE_TYPE = "exerciseType"  # Option contract exercise type (America/European)
    EXPIRATION_DATE = "expirationDate"
    EXPIRATION_TYPE = "expirationType"  # Expiration type (M, Q, S, W)
    EXTRINSIC_VALUE = "extrinsicValue"
    GAMMA = "gamma"  # Gamma Value
    HIGH_52_WEEK = "high52Week"  # Highest price traded in the past 12 months (52-week high)
    HIGH_PRICE = "highPrice"  # Day's high trade price
    IN_THE_MONEY = "inTheMoney"
    INTRINSIC_VALUE = "intrinsicValue"
    LAST = "last"  # Last traded price
    LAST_SIZE = "lastSize"  # Number of shares traded with last trade
    LAST_TRADING_DAY = "lastTradingDay"  # Last trading day (in milliseconds since epoch)
    LOW_52_WEEK = "low52Week"  # Lowest price traded in the past 12 months (52-week low)
    LOW_PRICE = "lowPrice"  # Day's low trade price
    MARK = "mark"  # Mark price
    MARK_CHANGE = "markChange"  # Mark Price change
    MARK_PERCENT_CHANGE = "markPercentChange"  # Mark Price percent change
    MINI = "mini"
    MULTIPLIER = "multiplier"  # Option multiplier
    NET_CHANGE = "netChange"  # Current Last-Prev Close
    NON_STANDARD = "nonStandard"
    OPEN_INTEREST = "openInterest"  # Open Interest
    OPEN_PRICE = "openPrice"  # Price at market open
    OPTION_DELIVERABLES_LIST = "optionDeliverablesList"
    OPTION_ROOT = "optionRoot"  # Underlying asset symbol
    PENNY_PILOT = "pennyPilot"  # Is this contract part of the Penny Pilot program
    PERCENT_CHANGE = "percentChange"
    PUT_CALL = "putCall"
    QUOTE_TIME_IN_LONG = "quoteTimeInLong"  # Last quote time in milliseconds since Epoch
    RHO = "rho"  # Rho Value
    SETTLEMENT_TYPE = "settlementType"  # Option contract settlement type (AM/PM)
    STRIKE_PRICE = "strikePrice"  # Strike Price
    SYMBOL = "symbol"  # Option contract symbol
    THEORETICAL_OPTION_VALUE = "theoreticalOptionValue"  # Theoretical option value
    THEORETICAL_VOLATILITY = "theoreticalVolatility"
    THETA = "theta"  # Theta Value
    TIME_VALUE = "timeValue"  # Time Value
    TOTAL_VOLUME = "totalVolume"  # Aggregated shares traded throughout the day
    TRADE_TIME_IN_LONG = "tradeTimeInLong"  # Last trade time in milliseconds since Epoch
    VEGA = "vega"  # Vega Value
    VOLATILITY = "volatility"  # Option risk/volatility measurement


# OptionDeliverables class
class OptionDeliverables:
    def __init__(
        self,
        symbol: str,
        assetType: str,
        deliverableUnits: str,
        currencyType: str = "USD",
    ):
        self.symbol: str = symbol
        self.assetType: str = assetType
        self.deliverableUnits: str = deliverableUnits
        self.currencyType: str = currencyType

    def to_dict(self) -> dict:
        """
        Converts an instance of OptionDeliverables to a dictionary.

        Returns:
            dict: Dictionary of OptionDeliverables class attributes.
        """
        return {
            "symbol": self.symbol,
            "assetType": self.assetType,
            "deliverableUnits": self.deliverableUnits,
            "currencyType": self.currencyType,
        }


# OptionContract class
class OptionContract:
    """
    Class for representing an option contract and with its various attributes.
    Some of the attributes are not defined per the API specification, rather
    what Schwab actually returns when requesting data.

    Attributes:
        ask (float): The current asking price for the option.
        askSize (int): The size of the ask order.
        bid (float): The current bid price for the option.
        bidAskSize (str): The combined size of bid and ask orders.
        bidSize (int): The size of the bid order.
        closePrice (float): The closing price of the option.
        daysToExpiration (float): The number of days until expiration.
        deliverableNote (str): Note on the deliverable assets.
        delta (float): The delta value of the option.
        description (str): Description of the option contract.
        exchangeName (str): Name of the exchange where the option is traded.
        exerciseType (str): Type of exercise for the option.
        expirationDate (str): Date when the option expires.
        expirationType (str): Type of expiration (e.g., American or European).
        extrinsicValue (float): The extrinsic value of the option.
        gamma (float): The gamma value of the option.
        high52Week (float): The highest price of the option in the last 52 weeks.
        highPrice (float): The highest price of the option during the current session.
        inTheMoney (bool): Indicates if the option is in the money.
        intrinsicValue (float): The intrinsic value of the option.
        last (float): The last traded price of the option.
        lastSize (int): The size of the last transaction.
        lastTradingDay (int): The timestamp of the last trading day.
        low52Week (float): The lowest price of the option in the last 52 weeks.
        lowPrice (float): The lowest price of the option during the current session.
        mark (float): The marked price of the option.
        markChange (float): The change in the marked price.
        markPercentChange (float): The percentage change in the marked price.
        mini (bool): Indicates if the option is a mini option.
        multiplier (int): The multiplier for the option.
        netChange (float): The net change in the option's price.
        nonStandard (bool): Indicates if the option is non-standard.
        openInterest (int): The open interest in the option.
        openPrice (float): The opening price of the option.
        optionDeliverablesList (dict): Dict of deliverables associated with the option.
        optionRoot (str): The root symbol of the option.
        pennyPilot (bool): Indicates if the option is part of the penny pilot program.
        percentChange (float): The percentage change in price.
        putCall (str): Indicates if the option is a put or a call.
        quoteTimeInLong (int): The timestamp of the quote in long format.
        rho (float): The rho value of the option.
        settlementType (str): The type of settlement for the option.
        strikePrice (float): The strike price of the option.
        symbol (str): The symbol of the option.
        theoreticalOptionValue (float): The theoretical value of the option.
        theoreticalVolatility (float): The theoretical volatility of the option.
        theta (float): The theta value of the option.
        timeValue (float): The time value of the option.
        totalVolume (int): The total volume of the option traded.
        tradeTimeInLong (int): The timestamp of the last trade in long format.
        vega (float): The vega value of the option.
        volatility (float): The implied volatility of the option.
    """

    def __init__(self):
        self.ask: float = 0.0
        self.askSize: int = 0
        self.bid: float = 0.0
        self.bidAskSize: str = None
        self.bidSize: int = 0
        self.closePrice: float = 0.0
        self.daysToExpiration: float = 0.0
        self.deliverableNote: str = None
        self.delta: float = 0.0
        self.description: str = None
        self.exchangeName: str = None
        self.exerciseType: str = None
        self.expirationDate: str = None
        self.expirationType: Optional[ExpirationType] = None
        self.extrinsicValue: float = 0.0
        self.gamma: float = 0.0
        self.high52Week: float = 0.0
        self.highPrice: float = 0.0
        self.inTheMoney: bool = False
        self.intrinsicValue: float = 0.0
        self.last: float = 0.0
        self.lastSize: int = 0
        self.lastTradingDay: int = 0
        self.low52Week: float = 0.0
        self.lowPrice: float = 0.0
        self.mark: float = 0.0
        self.markChange: float = 0.0
        self.markPercentChange: float = 0.0
        self.mini: bool = False
        self.multiplier: int = 0
        self.netChange: float = 0.0
        self.nonStandard: bool = False
        self.openInterest: int = 0
        self.openPrice: float = 0.0
        self.optionDeliverablesList: Dict[OptionDeliverables] = {}
        self.optionRoot: str = None
        self.pennyPilot: bool = False
        self.percentChange: float = 0.0
        self.putCall: str = None
        self.quoteTimeInLong: int = 0
        self.rho: float = 0.0
        self.settlementType: Optional[SettlementType] = None
        self.strikePrice: float = 0.0
        self.symbol: str = None
        self.theoreticalOptionValue: float = 0.0
        self.theoreticalVolatility: float = 0.0
        self.theta: float = 0.0
        self.timeValue: float = 0.0
        self.totalVolume: int = 0
        self.tradeTimeInLong: int = 0
        self.vega: float = 0.0
        self.volatility: float = 0.0

    @classmethod
    def from_dict(cls: Type["OptionContract"], data: dict) -> Type["OptionContract"]:
        """
        Creates an OptionContract instance from a dictionary.

        Args:
            cls (OptionContract): Class itself used to instantiate.
            data (dict): Dictionary containing raw option contract data.

        Returns:
            OptionContract: An instance of OptionContract with processed data.
        """
        instance = cls()
        # Schwab adds the contract data inside a single element list
        contract_data = data[0] if data else {}
        for key, value in contract_data.items():
            if hasattr(instance, key):
                if key == "optionDeliverablesList":
                    # Extract single nested element and use dictionary
                    data = OptionDeliverables(**value[0])
                    instance.optionDeliverablesList = data.to_dict()
                else:
                    setattr(instance, key, value)
        return instance

    def to_dict(self, keys: list[Enum] = None) -> dict:
        """
        Converts an OptionContract instance to a dictionary. By default,
        only select keys are utilized.

        Args:
            keys (list[str]): List of contract fields to keep.
        Returns:
            dict: Dictionary of OptionContract class attributes.
        """
        # For long options chains, the full map can add a lot of data.
        # The below serves as a means ot limit what data we care about.
        if keys is None:
            keys = [
                OptionContractFields.ASK,
                OptionContractFields.ASK_SIZE,
                OptionContractFields.BID,
                OptionContractFields.BID_SIZE,
                OptionContractFields.BID_ASK_SIZE,
                OptionContractFields.CLOSE_PRICE,
                OptionContractFields.DAYS_TO_EXPIRATION,
                OptionContractFields.DELTA,
                OptionContractFields.EXPIRATION_DATE,
                OptionContractFields.EXPIRATION_TYPE,
                OptionContractFields.GAMMA,
                OptionContractFields.IN_THE_MONEY,
                OptionContractFields.LAST,
                OptionContractFields.NON_STANDARD,
                OptionContractFields.OPEN_INTEREST,
                OptionContractFields.OPEN_PRICE,
                OptionContractFields.OPTION_ROOT,
                OptionContractFields.PERCENT_CHANGE,
                OptionContractFields.PUT_CALL,
                OptionContractFields.QUOTE_TIME_IN_LONG,
                OptionContractFields.RHO,
                OptionContractFields.STRIKE_PRICE,
                OptionContractFields.SYMBOL,
                OptionContractFields.THETA,
                OptionContractFields.TOTAL_VOLUME,
                OptionContractFields.VEGA,
                OptionContractFields.VOLATILITY,
            ]
        # Select all keys - note this requires a lot more storage for large chains
        elif keys == ["ALL"]:
            keys = list(OptionContractFields)

        return {
            key.value: getattr(self, key.value)
            for key in keys
            if hasattr(self, key.value)
        }


class Underlying:
    """
    A class representing an options contract underlying assets various
    attributes related to its trading and performance.

    Attributes:
        ask (float): The current asking price for the option.
        askSize (int): The number of contracts available at the asking price.
        bid (float): The current bidding price for the option.
        bidSize (int): The number of contracts available at the bidding price.
        change (float): The change in the option's price since the last trading
            session.
        close (float): The closing price of the option from the previous trading
            day.
        delayed (bool): Indicates whether the price data is delayed (True) or
            real-time (False).
        description (str, optional): A textual description of the option contract.
        exchangeName (Optional[ExchangeName]): The name of the exchange where the
            option is traded.
        fiftyTwoWeekHigh (float): The highest price of the option over the past
            52 weeks.
        fiftyTwoWeekLow (float): The lowest price of the option over the past 52
            weeks.
        highPrice (float): The highest price of the option during the current
            trading session.
        last (float): The last traded price of the option.
        lowPrice (float): The lowest price of the option during the current
            trading session.
        mark (float): The mark price of the option, which is an estimated fair
            value.
        markChange (float): The change in the mark price since the last trading
            session.
        markPercentChange (float): The percentage change in the mark price since
            the last trading session.
        openPrice (float): The opening price of the option for the current
            trading session.
        percentChange (float): The percentage change in the option's price from
            the previous trading session.
        quoteTime (int): The timestamp of the last price quote for the option.
        symbol (str, optional): The symbol representing the option contract.
        totalVolume (int): The total number of contracts traded during the
            current trading session.
        tradeTime (int): The timestamp of the last trade executed for the
            option.
    """

    def __init__(self):
        self.ask: float = 0.0
        self.askSize: int = 0
        self.bid: float = 0.0
        self.bidSize: int = 0
        self.change: float = 0.0
        self.close: float = 0.0
        self.delayed: bool = True
        self.description: str = None
        self.exchangeName: Optional[ExchangeName] = None
        self.fiftyTwoWeekHigh: float = 0.0
        self.fiftyTwoWeekLow: float = 0.0
        self.highPrice: float = 0.0
        self.last: float = 0.0
        self.lowPrice: float = 0.0
        self.mark: float = 0.0
        self.markChange: float = 0.0
        self.markPercentChange: float = 0.0
        self.openPrice: float = 0.0
        self.percentChange: float = 0.0
        self.quoteTime: int = 0
        self.symbol: str = None
        self.totalVolume: int = 0
        self.tradeTime: int = 0

    @classmethod
    def from_dict(cls: Type["Underlying"], data: dict) -> Type["Underlying"]:
        """
        Creates an Underlying instance from a dictionary.

        Args:
            cls (Underlying): Class itself used to instantiate.
            data (dict): Dictionary containing raw option contract data.

        Returns:
            Underlying: An instance of Underlying with processed data.
        """
        instance = cls()  # Instance of the class
        for k, v in data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        return instance

    def to_dict(self) -> dict:
        """
        Converts an instance of Underlying to a dictionary.

        Returns:
            dict: Dictionary of Underlying class attributes.
        """
        return {
            "ask": self.ask,
            "askSize": self.askSize,
            "bid": self.bid,
            "bidSize": self.bidSize,
            "change": self.change,
            "close": self.close,
            "delayed": self.delayed,
            "description": self.description,
            "exchangeName": self.exchangeName,
            "fiftyTwoWeekHigh": self.fiftyTwoWeekHigh,
            "fiftyTwoWeekLow": self.fiftyTwoWeekLow,
            "highPrice": self.highPrice,
            "last": self.last,
            "lowPrice": self.lowPrice,
            "mark": self.mark,
            "markChange": self.markChange,
            "markPercentChange": self.markPercentChange,
            "openPrice": self.openPrice,
            "percentChange": self.percentChange,
            "quoteTime": self.quoteTime,
            "symbol": self.symbol,
            "totalVolume": self.totalVolume,
            "tradeTime": self.tradeTime,
        }


class OptionChain:
    def __init__(self):
        self.symbol: str = None
        self.status: str = None
        self.underlying: dict = {}
        self.strategy: Strategy = None
        self.interval: float = 0.0
        self.isDelayed: bool = False
        self.isIndex: bool = False
        self.daysToExpiration: float = 0.0
        self.interestRate: float = 0.0
        self.underlyingPrice: float = 0.0
        self.volatility: float = 0.0
        self.numberOfContracts: str = None
        self.assetMainType: Optional[AssetMainType] = None
        self.assetSubType: Optional[AssetSubType] = None
        self.isChainTruncated: bool = False
        self.callExpDateMap: Dict[str, OptionContract] = {}
        self.putExpDateMap: Dict[str, OptionContract] = {}

    def _flatten_contract_chain(self, value: dict) -> dict:
        """
        Nested dictionary comprehension which flattens the contract map keys
        from YYYY-MM-DD:d, where d is days to expiration, to YYYY-MM-DD.P,
        where P is the contract strike price key.

        Args:
           value (dict): Option date map with nested dictionary of contracts.

        Returns:
            dict: Option date map dictionary with options contracts.
        """
        return {
            f"{date.split(':')[0]}.{contract}": OptionContract.from_dict(contract_data)
            for date, contracts in value.items()
            for contract, contract_data in contracts.items()
        }

    @classmethod
    def from_dict(cls: Type["OptionChain"], data: dict) -> Type["OptionChain"]:
        """
        Creates an instance of OptionChain from a dictionary.

        Args:
            cls (OptionChain): Class itself used to instantiate.
            data (dict): Dictionary containing raw option contract data.

        Returns:
            OptionChain: An instance of OptionChain with processed data.
        """
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                if key == "underlying":
                    underlying = Underlying.from_dict(value)
                    instance.underlying = underlying.to_dict()
                elif key == "strategy" and value in Strategy.__members__:
                    instance.strategy = Strategy[value]
                elif key == "callExpDateMap":
                    instance.callExpDateMap = instance._flatten_contract_chain(value)
                elif key == "putExpDateMap":
                    instance.putExpDateMap = instance._flatten_contract_chain(value)
                else:
                    setattr(instance, key, value)
        return instance

    # TODO: Set default behavior for contract fields
    def to_dict(self, contract_fields: list[str] = None) -> dict:
        """
        Converts an instance of OptionChain to a dictionary.

        Returns:
            dict: Dictionary of OptionChain class attributes.
        """
        callExpDateMap = {
            date: contract.to_dict(keys=contract_fields)
            for date, contract in self.callExpDateMap.items()
        }
        putExpDateMap = {
            date: contract.to_dict(keys=contract_fields)
            for date, contract in self.putExpDateMap.items()
        }
        return {
            "assetMainType": self.assetMainType,
            "assetSubType": self.assetSubType,
            "symbol": self.symbol,
            "status": self.status,
            "underlying": self.underlying,
            "strategy": self.strategy.value,
            "interval": self.interval,
            "isDelayed": self.isDelayed,
            "isIndex": self.isIndex,
            "daysToExpiration": self.daysToExpiration,
            "interestRate": self.interestRate,
            "underlyingPrice": self.underlyingPrice,
            "volatility": self.volatility,
            "isChainTruncated": self.isChainTruncated,
            "numberOfContracts": self.numberOfContracts,
            "callExpDateMap": callExpDateMap,
            "putExpDateMap": putExpDateMap,
        }

def concatenate_option_map(calls: Response, puts: Response)-> OptionChain:
    calls_dict = calls.json()
    puts_dict = puts.json()
    call_chain = OptionChain().from_dict(calls_dict)
    puts_chain = OptionChain().from_dict(puts_dict)
    call_chain.putExpDateMap = puts_chain.putExpDateMap
    return call_chain

# TODO: Handle condition where dict is None
def process_option_chain_response(
    data: dict, contract_fields: list[str] = None
) -> dict:
    """
    Receives an options response dictionary and preprocesses it.

    Args:
        data (dict): Equity response input

    Returns:
        dict: Dictionary of processed options response
    """
    option_chain = OptionChain().from_dict(data)
    return option_chain.to_dict(contract_fields)
