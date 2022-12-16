from dataclasses import dataclass


@dataclass
class Fund:
    id: int
    full_name: str
    ticker: str
    price: float
    currency: str
    lot: int
    average_profit: float
    commission: float
    average_overestimation: float
    average_volatility: float
    best_profit: float
    worst_profit: float


@dataclass
class Stock:
    fund_id: int
    name: str
    part: float
    type: str
