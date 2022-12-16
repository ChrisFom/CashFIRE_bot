from dataclasses import dataclass
import numpy as np

from db.db import DBLoader
from models.models import Fund


@dataclass
class ClientInfo:
    pass


@dataclass
class FundInfo:
    volatility: float
    avg_year_profit: float

    negative_profit_years: int
    total_years: int

    risk_level: float


def evaluate_funds(funds: list[FundInfo]):
    """ Оцениваем все фонды по риску и доходности """
    for fund in funds:
        fund.risk_level = count_fund_risk_level(fund)


def count_fund_risk_level(fund: FundInfo) -> float:
    """ Возвращает для фонда его уровень риска """
    risk_level = 0.6 * fund.negative_profit_years / fund.total_years + 0.4 * fund.volatility
    return risk_level


def predict_next_year_profit():
    """ Предсказываем для фонда доходность в следующем году """


def fund_ranking_function():
    """ """
    return


def get_finds_info() -> list[Fund]:
    loader = DBLoader()
    funds_info = loader.load_funds()

    return funds_info
