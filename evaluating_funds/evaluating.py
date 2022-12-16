from pprint import pprint

import numpy as np

from db.db import DBLoader
from models.models import Fund, Client


def evaluate_funds_rating(funds: list):  # -> list[Fund]:
    """ Оцениваем все фонды по риску и доходности """
    funds_ratings = dict()
    for fund in funds:
        fund.count_risk_level()
        fund_id = fund.id
        name = fund.full_name
        rating = fund_ranking_function(fund)
        profit = fund.average_profit
        volatility = fund.average_volatility
        risk_level = fund.risk_level
        funds_ratings[fund_id] = dict(name=name,
                                      profit=profit,
                                      volatility=volatility,
                                      risk_level=risk_level,
                                      rating=rating)
    return funds_ratings


def evaluate_personal_rating(categories: list[str], funds_ratings):
    """ Считает рейтинг фондов, учитывая предпочтительные категории клиента """
    return


def get_personal_funds(client: Client, funds: list[Fund]) -> dict[int, float]:
    """ Возвращает персонализированные рекомендации фондов для клиента, основываясь на предпочтительных категориях """
    personal_categories = client.categories
    funds_ratings = evaluate_funds_rating(funds=funds)
    personal_ratings = evaluate_personal_rating(categories=personal_categories,
                                                funds_ratings=funds_ratings)

    return {0: 0.5}


def predict_next_year_profit():
    """ Предсказываем для фонда доходность в следующем году """


def fund_ranking_function(fund: Fund) -> float:
    """ """
    risk_level = fund.risk_level
    profit = fund.average_profit

    rating = sigmoid(10 * profit / risk_level)
    return rating


def sigmoid(value):
    return 1 / (1 + 0.5 * np.exp(- (value - 5)))


def get_finds_info() -> list[Fund]:
    loader = DBLoader()
    funds_info = loader.load_funds()

    return funds_info


if __name__ == "__main__":
    funds = get_finds_info()
    client = Client(years_before_retirement=20,
                    expenses_per_month=50000,
                    categories=['healthcare', 'it', 'consumer_goods'])
    personal_funds = get_personal_funds(client=client,
                                        funds=funds)

    pprint(personal_funds)
