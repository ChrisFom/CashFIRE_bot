import logging

from db.db import DBLoader
from models.models import Client, Fund


class Evaluator:

    def get_personal_funds(self, client, funds: list) -> dict[int: float]:
        return {5: 0.33, 6: 0.33, 7: 0.34}


class Controller:

    def __init__(self):
        self._loader = DBLoader()
        self.evaluator = Evaluator()

    def get_personal_funds(self, client: Client):
        funds = self._loader.load_funds()
        return self.evaluator.get_personal_funds(client, funds)

    def get_text_about_stocks(self, client: Client, funds: list[Fund]) -> str:
        fire_number = (client.expenses_per_month * 12 / 0.04)
        average_profit = sum(
            self._search_fund_by_id(funds, key).average_profit * value
            for key, value
            in client.personal_funds.items()
        )
        yearly = fire_number / client.years_before_retirement / ((1 + average_profit) ** client.years_before_retirement)
        final_text = ''
        for id, weight in client.personal_funds.items():
            fund_info = self._search_fund_by_id(funds, id)
            final_text += f'{int(yearly / 60 * 0.3 / 12 / fund_info.price)} паев фонда {fund_info.full_name} \n'
        return f'\nДо пенсии осталось {client.years_before_retirement} лет\n' \
               f'Ежемесячные траты составляют {client.expenses_per_month} рублей\n' \
               f'Без учета сложного процента надо откладывать {int(fire_number/client.years_before_retirement)} рублей в год\n' \
               f'С учетом сложного процента надо откладывать {int(yearly)} рублей в год\n\n' \
               f'Для соответствия инвестиционному плану в этом месяце надо купить: \n' \
               f'{final_text}'

    def _search_fund_by_id(self, funds, id) -> Fund:
        for fund in funds:
            if fund.id == id:
                return fund
        logging.warning(f'No fund by id {id}')
