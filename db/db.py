from dataclasses import dataclass

import psycopg2
from psycopg2.extras import RealDictCursor

from config import config


@dataclass
class Fund:
    id: int
    full_name: str
    ticker: str
    price: float
    currency: str
    lot: int


connection = psycopg2.connect(**config)
cursor = connection.cursor(cursor_factory=RealDictCursor)
cursor.execute('SELECT * from stocks')
raw_records = cursor.fetchall()
cursor.close()
connection.close()

records = [
    Fund(
        id=record['id_fund'],
        full_name=record['full_fund'],
        ticker=record['short_fund'],
        price=record['price'],
        currency=record['currency'],
        lot=record['count_1_lot'],
    )
    for record
    in raw_records
]

print(records)
