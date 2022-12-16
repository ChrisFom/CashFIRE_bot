from dataclasses import dataclass, field


@dataclass
class Client:
    years_before_retirement: int = 0
    expenses_per_month: int = 0
    categories: list[str] = field(default_factory=list)
    personal_funds: dict = field(default_factory=dict)


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

    risk_level: float = 1000

    def count_risk_level(self, profit_coef: float = 0.6,
                         volatility_coef: float = 0.4) -> None:
        """ Вычисляет уровень риска фонда """
        if self.negative_years is not None:
            self.risk_level = profit_coef * self.negative_years / (
                    self.negative_years + self.positive_years) + volatility_coef * self.average_volatility


@dataclass
class Stock:
    fund_id: int
    name: str
    part: float
    type: str
