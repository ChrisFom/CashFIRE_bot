from pprint import pprint
from typing import Union

import numpy as np

from data_source.data_loaders import DBLoader
from models.models import Fund, Client


class FundsRecommender:
    @staticmethod
    def get_personal_funds(client: Client, funds: list[Fund], top_n: int = 5) -> dict[int, float]:
        """ Возвращает персонализированные рекомендации фондов для клиента,
        основываясь на предпочтительных категориях
        """
        personal_categories = client.categories
        funds = add_categories_to_fund(funds=funds)
        funds_ratings = evaluate_funds_rating(funds=funds)
        personal_ratings = evaluate_personal_rating(categories=personal_categories,
                                                    funds_ratings=funds_ratings)
        sorted_personal_ratings = sort_funds_by_rating(personal_ratings)
        client_top_funds = sorted_personal_ratings[:top_n]
        client_top_funds = {item[0]: item[1]['rating'] for item in client_top_funds}
        return client_top_funds


def evaluate_funds_rating(funds: list[Fund]) -> dict[int, dict[str, Union[float, list[str]]]]:
    """ Возвращает отсортированный по рейтингу список id фондов """
    funds_ratings = dict()
    for fund in funds:
        fund.count_risk_level()
        rating = fund_ranking_function(fund)
        funds_ratings[fund.id] = dict(rating=rating,
                                      categories=fund.categories)
    return funds_ratings


def evaluate_personal_rating(categories: list[str],
                             funds_ratings: dict[int, dict[str, Union[float, list[str]]]]):
    """ Считает рейтинг фондов, учитывая предпочтительные категории клиента """
    for fund_id, fund_info in funds_ratings.items():
        number_of_categories = len(list(set(fund_info['categories']) & set(categories)))
        fund_info['rating'] *= number_of_categories + 1
    return funds_ratings


def sort_funds_by_rating(funds_ratings: dict[int, dict[str, Union[float, list[str]]]]):
    return sorted(funds_ratings.items(), key=lambda k: k[1]['rating'], reverse=True)


def add_categories_to_fund(funds: list[Fund]) -> list[Fund]:
    loader = DBLoader()
    categories = loader.load_categories_of_funds()
    for fund in funds:
        fund.categories = categories[fund.id]

    return funds


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
    recommender = FundsRecommender()
    personal_funds = recommender.get_personal_funds(client=client,
                                                    funds=funds)

    pprint(personal_funds)
