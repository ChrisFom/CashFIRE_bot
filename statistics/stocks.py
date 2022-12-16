from collections import defaultdict

from db.db import DBLoader

funds_weights = {5: 0.33, 6: 0.33, 7: 0.34}

counter = defaultdict(float)
loader = DBLoader()
stocks = loader.load_stocks()
for stock in stocks:
    if stock.fund_id in funds_weights:
        stock.part *= funds_weights[stock.fund_id]
    else:
        stock.part = 0
sum_of_stocks = sum(stock.part for stock in stocks)
for stock in stocks:
    counter[stock.name] += stock.part / sum_of_stocks
print(sorted(counter.items(), key=lambda item: item[1], reverse=True))
