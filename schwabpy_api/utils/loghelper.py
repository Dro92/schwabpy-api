from enum import Enum
from datetime import datetime

from schwabpy_api.processing.options_processing import OptionChain


class LoggingDescriptor(Enum):
    OPTION_QUOTE = "OPTION_QUOTE"
    EQUITY_QUOTE = "EQUITY_QUOTE"


class LoggableData:
    def to_dict(self):
        """Convert public attributes to dictionary."""
        # """Convert data to dictionary. To be implemented by subclass."""
        # Return only public attributes
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}



class LogOptionsMetrics(LoggableData):
    def __init__(
        self,
        request_time: datetime,
        data: OptionChain,
        response_time: float
    ):
        #  Time which request was sent
        self.assetType = LoggingDescriptor.OPTION_QUOTE.value
        self.requestTime = request_time
        self.responseTime = response_time  # Time from request to receive
        self.symbol = "NOTSET"
        self.callCount = 0
        self.putCount = 0
        self._process_data(data)

    def _process_data(self, data: OptionChain) -> None:
        # TODO: Really need to do something about these magic strings.
        # TODO: Create proper enum classes to handle all these?
        symbol = "symbol"
        calls = "callExpDateMap"
        puts = "putExpDateMap"
        data = data.to_dict()
        
        if symbol in data:
            self.symbol = data[symbol]

        # Count call contracts
        self.callCount = len(data[calls])

        # Count put contracts
        self.putCount = len(data[puts])




class LogEquitiesMetrics(LoggableData):
    def __init__(
        self,
        request_time: datetime,
        data: dict,
        response_time: float
    ):
        #  Time which request was sent
        self.assetType = LoggingDescriptor.EQUITY_QUOTE.value
        self.requestTime = request_time
        self.responseTime = response_time  # Time from request to receive
        self.equityCount = len(data)
        # TODO: Does adding ticker data here make any sense?
        # Equity responses can have multuple symbols.