from pprint import pprint
from typing import Union

import numpy as np
from pathlib import Path
from data_source.data_loaders import DBLoader
from models.models import Fund, Client
from risk_models.risk_models import RiskModel, fit_model, get_funds_info


class FundsRecommender:
    def __init__(self):
        self.risk_model = RiskModel()
        model_default_path: Path = Path('../pretrained_models/risk_model.pkl')
        if model_default_path.exists():
            self.risk_model.load_model(model_path=model_default_path)
        else:
            self.risk_model = fit_model()

    def get_personal_funds(self, client: Client,
                           funds: list[Fund],
                           top_n: int = 5,
                           use_risk_model: bool = True) -> dict[int, float]:
        """ Возвращает персонализированные рекомендации фондов для клиента, основываясь на предпочтительных категориях
        params:
            client: Client - информация про клиента из бота
            funds: list[Fund] - информация о фондах из БД
            top_n: int - количество рекомендаций для выдачи пользователю
            use_risk_model: bool - флаг использовать логистическую регрессию или функцию для оценки риска (по умолчанию True)
        """
        personal_categories = client.categories
        funds = add_categories_to_fund(funds=funds)
        funds_ratings = self._evaluate_funds_rating(funds=funds, use_risk_model=use_risk_model)
        personal_ratings = evaluate_personal_rating(categories=personal_categories,
                                                    funds_ratings=funds_ratings)
        sorted_personal_ratings = sort_funds_by_rating(personal_ratings)
        client_top_funds = sorted_personal_ratings[:top_n]
        client_top_funds = {item[0]: item[1]['rating'] for item in client_top_funds}
        return client_top_funds

    def _evaluate_funds_rating(self, funds: list[Fund], use_risk_model: bool = True) -> dict[
        int, dict[str, Union[float, list[str]]]]:
        """ Возвращает отсортированный по рейтингу список id фондов """
        funds_ratings = dict()
        for fund in funds:
            if use_risk_model:
                features_data = np.array([fund.price,
                                          fund.average_profit,
                                          fund.average_volatility,
                                          fund.positive_years,
                                          fund.negative_years])
                features_data = np.where(features_data == None, 0, features_data)
                fund.risk_level = self.risk_model.predict(features_data)
            else:
                fund.default_count_risk_level()
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


if __name__ == "__main__":
    funds = get_funds_info()
    client = Client(years_before_retirement=20,
                    expenses_per_month=50000,
                    categories=['healthcare', 'it', 'consumer_goods'])
    recommender = FundsRecommender()
    personal_funds = recommender.get_personal_funds(client=client,
                                                    funds=funds)

    pprint(funds)
