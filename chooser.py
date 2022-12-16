from dataclasses import dataclass
from typing import Optional


@dataclass
class Client:
    years_before_retirement: Optional[int] = None
    expenses_per_month: Optional[int] = None


@dataclass
class Fund:
    name: str
    average_profit: float
    price: float
    countries: Optional[dict] = None
    industries: Optional[dict] = None
    types: Optional[dict] = None
    stocks: Optional[dict] = None


client = Client(
    years_before_retirement=10,
    expenses_per_month=100_000,
)

biotech_fund = Fund(
    name='TBIO',
    average_profit=10.2,
    price=0.0816,
)

technology_fund = Fund(
    name='TECH',
    average_profit=13.2,
    price=0.1035,
)


class Chooser:
    """Класс для выбора фондов в нужном соотношении."""

    def get_text_about_stocks(self, client: Client) -> str:
        fire_number = (client.expenses_per_month * 12 / 0.04)
        average_profit = (0.3 * biotech_fund.average_profit + 0.7 * technology_fund.average_profit)
        yearly = fire_number / client.years_before_retirement / (
                    (1 + (average_profit / 100)) ** client.years_before_retirement)
        return f'\nДо пенсии осталось {client.years_before_retirement} лет\n' \
               f'Ежемесячные траты составляют {client.expenses_per_month} рублей\n' \
               f'Без учета сложного процента надо откладывать {int(fire_number / client.years_before_retirement)} рублей в год\n' \
               f'С учетом сложного процента надо откладывать {int(yearly)} рублей в год\n\n' \
               f'Для соответствия инвестиционному плану в этом месяце надо купить: \n' \
               f'{int(yearly / 60 * 0.3 / 12 / biotech_fund.price)} паев фонда {biotech_fund.name} \n' \
               f'{int(yearly / 60 * 0.7 / 12 / technology_fund.price)} паев фонда {technology_fund.name}'
