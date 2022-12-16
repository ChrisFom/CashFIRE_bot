import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from models.models import Fund, Stock

load_dotenv()


class DBLoader:
    def __init__(self):
        self._connection_config: dict = dict(
            database=os.environ['DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['PASSWORD'],
            host=os.environ['HOST'],
            port=os.environ['PORT'],
        )

    def _load_sql(self, query: str) -> list:
        connection = psycopg2.connect(**self._connection_config)

        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        raw_records = cursor.fetchall()
        cursor.close()
        connection.close()

        return raw_records

    def load_stocks(self) -> list[Stock]:
        """Загружает информацию об акциях из БД."""
        raw_records = self._load_sql('''SELECT * FROM stocks''')
        return [
            Stock(
                fund_id=int(record['id_fund']),
                name=record['stock_name'],
                part=record['part'],
                type=record['type'],
            )
            for record
            in raw_records
        ]

    def load_funds(self) -> list[Fund]:
        """Загружает информацию о фондах из БД."""
        raw_records = self._load_sql('''SELECT * FROM funds''')
        return [
            Fund(
                id=record['id'],
                full_name=record['full_fund'],
                ticker=record['ticker'],
                price=record['price'],
                currency=record['currency'],
                lot=record['lot'],
                average_profit=record['avg_profit'],
                best_profit=record['best_profit'],
                worst_profit=record['worst_profit'],
                commission=record['commission'],
                average_volatility=record['avg_volatility'],
                average_overestimation=record['avg_overestimation'],
                positive_years=record['positive_years'],
                negative_years=record['negative_years']
            )
            for record
            in raw_records
        ]

    def load_field_of_stock(self):
        """ Возвращает словарь с id фонда и списком отраслей  """
        raw_records = self._load_sql('''SELECT * FROM otrasl''')

        funds_fields = dict()

        records = {int(record['id_funds']): dict(consumer_goods=record['consumer_goods'],
                                                 currency=record['currency'],
                                                 eco_houses=record['eco_houses'],
                                                 eco_materials=record['eco_materials'],
                                                 electrotransport=record['electrotransport'],
                                                 energetics=record['energetics'],
                                                 finance=record['finance'],
                                                 green_energetics=record['green_energetics'],
                                                 healthcare=record['healthcare'],
                                                 houses=record['houses'],
                                                 it=record['it'],
                                                 luxury_metals=record['luxury_metals'],
                                                 machinery=record['machinery'],
                                                 materials=record['materials'],
                                                 obligations=record['obligations'],
                                                 other=record['other'],
                                                 telecommunications=record['telecommunications'])
                   for record in raw_records}
        for fund_id, parts in records.items():
            categories = []
            for category, part in parts.items():
                if part > 0:
                    categories.append(category)
            funds_fields[fund_id] = categories

        return funds_fields
