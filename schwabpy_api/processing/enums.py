from enum import Enum


class AssetMainType(Enum):
    BOND = "BOND"
    EQUITY = "EQUITY"
    FOREX = "FOREX"
    FUTURE = "FUTURE"
    FUTURE_OPTION = "FUTURE_OPTION"
    INDEX = "INDEX"
    MUTUAL_FUND = "MUTUAL_FUND"
    OPTION = "OPTION"


class AssetSubType(Enum):
    COE = "COE"  # Common Equity
    PRF = "PRF"  # Preferred Stock
    ADR = "ADR"  # American Depositary Receipt
    GDR = "GDR"  # Global Depositary Receipt
    CEF = "CEF"  # Closed-End Fund
    ETF = "ETF"  # Exchange-Traded Fund
    ETN = "ETN"  # Exchange-Traded Note
    UIT = "UIT"  # Unit Investment Trust
    WAR = "WAR"  # Warrants
    RGT = "RGT"  # Rights
