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


def evaluate_funds(funds: list[Fund]):
    """ Оцениваем все фонды по риску и доходности """
    for fund in funds:
        fund.count_risk_level()


def predict_next_year_profit():
    """ Предсказываем для фонда доходность в следующем году """


def fund_ranking_function():
    """ """
    return


def get_finds_info() -> list[Fund]:
    loader = DBLoader()
    funds_info = loader.load_funds()

    return funds_info
