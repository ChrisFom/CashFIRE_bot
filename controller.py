import logging

from data_source.data_loaders import DBLoader
from models.models import Client, Fund
from recommenders.recommenders import FundsRecommender


class Controller:

    def __init__(self):
        self._loader = DBLoader()
        self.evaluator = FundsRecommender()

    def get_personal_funds(self, client: Client):
        self.funds = self._loader.load_funds()
        return self.evaluator.get_personal_funds(client, self.funds)

    def get_text_about_stocks(self, client: Client) -> str:
        fire_number = (client.expenses_per_month * 12 / 0.04)
        average_profit = sum(
            self._search_fund_by_id(self.funds, key).average_profit * value
            for key, value
            in client.personal_funds.items()
        )
        yearly = fire_number / client.years_before_retirement / ((1 + average_profit) ** client.years_before_retirement)
        final_text = ''
        for id, weight in client.personal_funds.items():
            fund_info = self._search_fund_by_id(self.funds, id)
            final_text += f'{int(yearly / 60 * 0.3 / 12 / fund_info.price)} паев фонда {fund_info.full_name}' \
                          f'с доходностью {fund_info.average_profit} %\n'
        return f'\nДо пенсии осталось {client.years_before_retirement} лет\n' \
               f'Ежемесячные траты составляют {client.expenses_per_month} рублей\n' \
               f'Без учета сложного процента надо откладывать {int(fire_number / client.years_before_retirement)} рублей в год\n' \
               f'С учетом сложного процента надо откладывать {int(yearly)} рублей в год\n' \
               f'Ожидаемая доходность: {average_profit}\n\n' \
               f'Для соответствия инвестиционному плану в этом месяце надо купить: \n' \
               f'{final_text}'

    def _search_fund_by_id(self, funds, id) -> Fund:
        for fund in funds:
            if fund.id == id:
                return fund
        logging.warning(f'No fund by id {id}')
