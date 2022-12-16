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
    positive_years: int
    negative_years: int

    risk_level: float

    def count_risk_level(self, profit_coef: float = 0.6,
                         volatility_coef: float = 0.4) -> None:
        """ Вычисляет уровень риска фонда """
        self.risk_level = profit_coef * self.negative_years / (
                self.negative_years + self.positive_years) + volatility_coef * self.average_volatility

@dataclass
class Stock:
    fund_id: int
    name: str
    part: float
    type: str