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
        raw_records = self._load_sql('''SELECT * FROM stocks''')
        return [
            Stock(
                fund_id=record['id_fund'],
                name=record['stock_name'],
                part=record['part'],
                type=record['type'],
            )
            for record
            in raw_records
        ]

    def load_funds(self) -> list[Fund]:
        """ Загружает информацию о фондах из БД """
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
            )
            for record
            in raw_records
        ]
