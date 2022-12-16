import os
from dataclasses import dataclass

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


load_dotenv()


@dataclass
class Fund:
    full_name: str
    ticker: str
    price: float
    currency: str
    lot: int
    average_profit: float
    commission: float
    average_overestimation: float
    average_volatility: float
    best_profit: float
    worst_profit: float


connection = psycopg2.connect(
    database=os.environ['DATABASE'],
    user=os.environ['DB_USER'],
    password=os.environ['PASSWORD'],
    host=os.environ['HOST'],
    port=os.environ['PORT'],
)
cursor = connection.cursor(cursor_factory=RealDictCursor)
cursor.execute('SELECT * from funds')
raw_records = cursor.fetchall()
cursor.close()
connection.close()

records = [
    Fund(
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

print(records)
