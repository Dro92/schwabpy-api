from enum import Enum
from typing import Optional, Type

from schwabpy_api.processing.enums import AssetMainType, AssetSubType


class QuoteType(Enum):
    """
    Type of quote received.
    """

    NBBO = "NBBO"  # National Best Bid and Offer
    NFL = "NFL"  # Non-fee liable


class DivFreq(Enum):
    """
    Enum representing the frequency of dividend payments.
    """

    ANNUAL = 1  # Annually
    SEMI_ANNUAL = 2  # Semi-annually
    THREE_TIMES = 3  # Three times a year
    QUARTERLY = 4  # Quarterly
    EVERY_OTHER_MONTH = 6  # Every other month
    ELEVEN_TIMES = 11  # Eleven times a year
    MONTHLY = 12  # Monthly


class FundStrategy(Enum):
    """
    Enum representing the strategy of a fund.
    """

    ACTIVE = "A"  # Active
    LEVERAGED = "L"  # Leveraged
    PASSIVE = "P"  # Passive
    QUANTITATIVE = "Q"  # Quantitative
    SHORT = "S"  # Short


class EquityQuote:
    """
    Quote information of an equity security.

    Attributes:
        week52High (float): Highest price traded in the past 12 months or 52 weeks.
        week52Low (float): Lowest price traded in the past 12 months or 52 weeks.
        askMICId (Optional[str]): MIC code for ask.
        askPrice (float): Current best ask price.
        askSize (int): Number of shares for ask.
        askTime (int): Last ask time in milliseconds since Epoch.
        bidMICId (Optional[str]): MIC code for bid.
        bidPrice (float): Current best bid price.
        bidSize (int): Number of shares for bid.
        bidTime (int): Last bid time in milliseconds since Epoch.
        closePrice (float): Previous day's closing price.
        highPrice (float): Day's high trade price.
        lastMICId (Optional[str]): MIC code for last trade.
        lastPrice (float): Last traded price.
        lastSize (int): Number of shares traded with the last trade.
        lowPrice (float): Day's low trade price.
        mark (float): Mark price.
        markChange (float): Mark price change.
        markPercentChange (float): Mark price percent change.
        netChange (float): Current last - previous close.
        netPercentChange (float): Net percentage change.
        openPrice (float): Price at market open.
        quoteTime (int): Last quote time in milliseconds since Epoch.
        securityStatus (Optional[str]): Status of security.
        totalVolume (int): Aggregated shares traded throughout the day.
        tradeTime (int): Last trade time in milliseconds since Epoch.
        volatility (float): Option risk/volatility measurement.
    """

    def __init__(self):
        self.week52High: float = 0.0
        self.week52Low: float = 0.0
        self.askMICId: Optional[str] = None
        self.askPrice: float = 0.0
        self.askSize: int = 0
        self.askTime: int = 0
        self.bidMICId: Optional[str] = None
        self.bidPrice: float = 0.0
        self.bidSize: int = 0
        self.bidTime: int = 0
        self.closePrice: float = 0.0
        self.highPrice: float = 0.0
        self.lastMICId: Optional[str] = None
        self.lastPrice: float = 0.0
        self.lastSize: int = 0
        self.lowPrice: float = 0.0
        self.mark: float = 0.0
        self.markChange: float = 0.0
        self.markPercentChange: float = 0.0
        self.netChange: float = 0.0
        self.netPercentChange: float = 0.0
        self.openPrice: float = 0.0
        self.quoteTime: int = 0
        self.securityStatus: Optional[str] = None
        self.totalVolume: int = 0
        self.tradeTime: int = 0
        self.volatility: float = 0.0

    def to_dict(self) -> dict:
        """
        Converts the EquityQuote instance to a dictionary.

        Returns:
            dict: A dictionary representation of the EquityQuote instance.
        """
        return {
            "week52High": self.week52High,
            "week52Low": self.week52Low,
            "askMICId": self.askMICId,
            "askPrice": self.askPrice,
            "askSize": self.askSize,
            "askTime": self.askTime,
            "bidMICId": self.bidMICId,
            "bidPrice": self.bidPrice,
            "bidSize": self.bidSize,
            "bidTime": self.bidTime,
            "closePrice": self.closePrice,
            "highPrice": self.highPrice,
            "lastMICId": self.lastMICId,
            "lastPrice": self.lastPrice,
            "lastSize": self.lastSize,
            "lowPrice": self.lowPrice,
            "mark": self.mark,
            "markChange": self.markChange,
            "markPercentChange": self.markPercentChange,
            "netChange": self.netChange,
            "netPercentChange": self.netPercentChange,
            "openPrice": self.openPrice,
            "quoteTime": self.quoteTime,
            "securityStatus": self.securityStatus,
            "totalVolume": self.totalVolume,
            "tradeTime": self.tradeTime,
            "volatility": self.volatility,
        }


class ExtendedMarket:
    """
    Represents quote data for extended market hours.

    Attributes:
        askPrice (float): Extended market ask price.
        askSize (int): Extended market ask size.
        bidPrice (float): Extended market bid price.
        bidSize (int): Extended market bid size.
        lastPrice (float): Extended market last price.
        lastSize (int): Regular market last size.
        mark (float): Mark price.
        quoteTime (int): Extended market quote time in milliseconds since Epoch.
        totalVolume (int): Total volume.
        tradeTime (int): Extended market trade time in milliseconds since Epoch.
    """

    def __init__(self):
        self.askPrice: float = 0.0
        self.askSize: int = 0
        self.bidPrice: float = 0.0
        self.bidSize: int = 0
        self.lastPrice: float = 0.0
        self.lastSize: int = 0
        self.mark: float = 0.0
        self.quoteTime: int = 0
        self.totalVolume: int = 0
        self.tradeTime: int = 0

    def to_dict(self) -> dict:
        """
        Converts the ExtendedMarket instance to a dictionary.

        Returns:
            dict: A dictionary representation of the ExtendedMarket instance.
        """
        return {
            "askPrice": self.askPrice,
            "askSize": self.askSize,
            "bidPrice": self.bidPrice,
            "bidSize": self.bidSize,
            "lastPrice": self.lastPrice,
            "lastSize": self.lastSize,
            "mark": self.mark,
            "quoteTime": self.quoteTime,
            "totalVolume": self.totalVolume,
            "tradeTime": self.tradeTime,
        }


class Fundamental:
    """
    Represents the fundamental data of a security.

    Attributes:
        avg10DaysVolume (float): Average trading volume over the last 10 days.
        avg1YearVolume (float): Average trading volume over the last year.
        declarationDate (str): Declaration date in the format yyyy-MM-dd'T'HH:mm:ssZ.
        divAmount (float): Dividend amount.
        divExDate (str): Ex-dividend date in the format yyyy-MM-dd'T'HH:mm:ssZ.
        divFreq (Optional[DivFreq]): Frequency of dividend payments (represented by DivFreq enum).
        divPayAmount (float): Amount of the dividend payment.
        divPayDate (str): Dividend pay date in the format yyyy-MM-dd'T'HH:mm:ssZ.
        divYield (float): Dividend yield.
        eps (float): Earnings per share.
        fundLeverageFactor (float): Leverage factor of the fund.
        fundStrategy (Optional[FundStrategy]): Strategy of the fund (represented by FundStrategy enum).
        nextDivExDate (str): Next ex-dividend date in the format yyyy-MM-dd'T'HH:mm:ssZ.
        nextDivPayDate (str): Next dividend pay date in the format yyyy-MM-dd'T'HH:mm:ssZ.
        peRatio (float): Price-to-earnings ratio.
    """

    def __init__(self):
        self.avg10DaysVolume: float = 0.0
        self.avg1YearVolume: float = 0.0
        self.declarationDate: str = None
        self.divAmount: float = 0.0
        self.divExDate: str = None
        self.divFreq: Optional[DivFreq] = None
        self.divPayAmount: float = 0.0
        self.divPayDate: str = None
        self.divYield: float = 0.0
        self.eps: float = 0.0
        self.fundLeverageFactor: float = 0.0
        self.fundStrategy: Optional[FundStrategy] = None
        self.nextDivExDate: str = None
        self.nextDivPayDate: str = None
        self.peRatio: float = 0.0

    def to_dict(self) -> dict:
        """
        Converts the Fundamental instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Fundamental instance.
        """
        return {
            "avg10DaysVolume": self.avg10DaysVolume,
            "avg1YearVolume": self.avg1YearVolume,
            "declarationDate": self.declarationDate,
            "divAmount": self.divAmount,
            "divExDate": self.divExDate,
            "divFreq": self.divFreq.name if self.divFreq else None,
            "divPayAmount": self.divPayAmount,
            "divPayDate": self.divPayDate,
            "divYield": self.divYield,
            "eps": self.eps,
            "fundLeverageFactor": self.fundLeverageFactor,
            "fundStrategy": self.fundStrategy.name if self.fundStrategy else None,
            "nextDivExDate": self.nextDivExDate,
            "nextDivPayDate": self.nextDivPayDate,
            "peRatio": self.peRatio,
        }


class ReferenceEquity:
    """
    Represents the reference data of an equity security.

    Attributes:
        cusip (str): CUSIP of the instrument.
        description (str): Description of the instrument.
        exchange (str): Exchange code.
        exchangeName (str): Name of the exchange.
        fsiDesc (Optional[str]): FSI description (limited to 50 characters).
        htbQuantity (int): Hard-to-borrow quantity.
        htbRate (float): Hard-to-borrow rate.
        isHardToBorrow (bool): Indicates if the security is hard to borrow.
        isShortable (bool): Indicates if the security is shortable.
        otcMarketTier (Optional[str]): OTC market tier (up to 10 characters).
    """

    def __init__(self):
        self.cusip: str = None
        self.description: str = None
        self.exchange: str = None
        self.exchangeName: str = None
        self.fsiDesc: Optional[str] = None
        self.htbQuantity: int = 0
        self.htbRate: float = 0.0
        self.isHardToBorrow: bool = False
        self.isShortable: bool = False
        self.otcMarketTier: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Converts the ReferenceEquity instance to a dictionary.

        Returns:
            dict: A dictionary representation of the ReferenceEquity instance.
        """
        return {
            "cusip": self.cusip,
            "description": self.description,
            "exchange": self.exchange,
            "exchangeName": self.exchangeName,
            "fsiDesc": self.fsiDesc,
            "htbQuantity": self.htbQuantity,
            "htbRate": self.htbRate,
            "isHardToBorrow": self.isHardToBorrow,
            "isShortable": self.isShortable,
            "otcMarketTier": self.otcMarketTier,
        }


class RegularMarket:
    """
    Represents the latest market information of a security.

    Attributes:
        regularMarketLastPrice (float): The last price in the regular market.
        regularMarketLastSize (int): The last size of the trade in the regular market.
        regularMarketNetChange (float): The net change in the regular market.
        regularMarketPercentChange (float): The percent change in the regular market.
        regularMarketTradeTime (int): The trade time in milliseconds since Epoch.
    """

    def __init__(self):
        self.regularMarketLastPrice: float = 0.0
        self.regularMarketLastSize: int = 0
        self.regularMarketNetChange: float = 0.0
        self.regularMarketPercentChange: float = 0.0
        self.regularMarketTradeTime: int = 0

    def to_dict(self) -> dict:
        """
        Converts the RegularMarket instance to a dictionary.

        Returns:
            dict: A dictionary representation of the RegularMarket instance.
        """
        return {
            "regularMarketLastPrice": self.regularMarketLastPrice,
            "regularMarketLastSize": self.regularMarketLastSize,
            "regularMarketNetChange": self.regularMarketNetChange,
            "regularMarketPercentChange": self.regularMarketPercentChange,
            "regularMarketTradeTime": self.regularMarketTradeTime,
        }


class EquityResponse:
    """
        Represents quote information for an equity security.

    Attributes:
        assetMainType (AssetMainType): The instrument's asset type.
        assetSubType (EquityAssetSubType): The asset sub-type (nullable).
        ssid (int): The SSID of the instrument.
        symbol (str): The symbol of the instrument.
        realtime (bool): Indicates whether the quote is realtime.
        quoteType (QuoteType): The type of quote (nullable).
        extended (ExtendedMarket): Extended market data.
        fundamental (Fundamental): Fundamental data of the equity.
        quote (QuoteEquity): Quote data of the equity.
        reference (ReferenceEquity): Reference data of the equity.
        regular (RegularMarket): Regular market data.
    """

    def __init__(self):
        self.assetMainType: Optional[AssetMainType] = None
        self.assetSubType: Optional[AssetSubType] = None
        self.ssid: int = 0
        self.symbol: Optional[str] = None
        self.realtime: bool = False
        self.quoteType: Optional[QuoteType] = None
        self.extended: Optional[ExtendedMarket] = None
        self.fundamental: Optional[Fundamental] = None
        self.quote: Optional[EquityQuote] = None
        self.reference: Optional[ReferenceEquity] = None
        self.regular: Optional[RegularMarket] = None

    @classmethod
    def from_dict(cls: Type["EquityResponse"], data: dict) -> Type["EquityResponse"]:
        """
        Creates an EquityResponse instance from a dictionary.

        Args:
            cls (EquityResponse): Class itself used to instantiate.
            data (dict): Dictionary containing raw option contract data.

        Returns:
            EquityResponse: An instance of EquityResponse with processed data.
        """
        instance = cls()  # Instance of the class
        for k, v in data.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        return instance

    def to_dict(self) -> dict:
        """
        Converts the EquityResponse instance to a dictionary.

        Returns:
            dict: A dictionary representation of the EquityResponse instance.
        """
        return {
            "assetMainType": self.assetMainType,
            "assetSubType": self.assetSubType,
            "ssid": self.ssid,
            "symbol": self.symbol,
            "realtime": self.realtime,
            "quoteType": self.quoteType,
            "extended": self.extended,
            "fundamental": self.fundamental,
            "quote": self.quote,
            "reference": self.reference,
            "regular": self.regular,
        }


def process_equity_response(data: dict) -> dict:
    """
    Receives an equity response dictionary and preprocesses it.

    Args:
        data (dict): Equity response input

    Returns:
        dict: Dictionary of processed Equity response
    """
    response = {}
    for ticker, equity_data in data.items():
        equity_data = EquityResponse.from_dict(equity_data)
        response[ticker] = equity_data.to_dict()
    return response
