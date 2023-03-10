import logging

from data_source.data_loaders import DBLoader
from models.models import Client, Fund
from recommenders.recommenders import FundsRecommender
from utils.inflation import INFLATION_RATE


class Controller:

    def __init__(self):
        self._loader = DBLoader()
        self.evaluator = FundsRecommender()

    def get_personal_funds(self, client: Client):
        self.funds = self._loader.load_funds()
        return self.evaluator.get_personal_funds(client, self.funds)

    def get_text_about_stocks(self, client: Client) -> str:
        inflation_expenses_per_month = (client.expenses_per_month * (INFLATION_RATE**client.years_before_retirement))
        fire_number = (inflation_expenses_per_month * 12 / 0.04)
        average_profit = sum(
            self._search_fund_by_id(self.funds, key).average_profit * value
            for key, value
            in client.personal_funds.items()
        )
        yearly = fire_number / client.years_before_retirement / ((1 + average_profit) ** client.years_before_retirement)
        final_text = ''
        strategy_text = ''
        for id, weight in client.personal_funds.items():
            fund_info = self._search_fund_by_id(self.funds, id)
            strategy_text += f'{fund_info.ticker} - {round(weight*100, 1) }% ; '
            final_text += f'{int(yearly / 60 * 0.3 / 12 / fund_info.price)} паев фонда {fund_info.full_name}' \
                          f' ( доходность {round(fund_info.average_profit*100, 1)} % )\n'
        return f'\nДо пенсии осталось {client.years_before_retirement} лет\n' \
               f'Ежемесячные траты составляют {client.expenses_per_month} рублей\n' \
               f'Ежемесячные траты с учетом инфляции составят {inflation_expenses_per_month}\n' \
               f'Без учета сложного процента надо откладывать {int(fire_number / client.years_before_retirement)} рублей в год\n' \
               f'С учетом сложного процента надо откладывать {int(yearly)} рублей в год\n' \
               f'Ожидаемая доходность: {round(average_profit*100, 1)} % в год\n\n' \
               f'Инвестиционная стратегия: {strategy_text} \n\n' \
               f'Для соответствия инвестиционному плану в этом месяце надо купить: \n' \
               f'{final_text}'

    def _search_fund_by_id(self, funds, id) -> Fund:
        for fund in funds:
            if fund.id == id:
                return fund
        logging.warning(f'No fund by id {id}')
