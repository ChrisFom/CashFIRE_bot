from collections import defaultdict

from db.db import DBLoader
from models.models import Stock


class StocksStatistics:

    _loader = DBLoader()

    def get_top_stocks(self, weights: dict[int, float], n_top: int) -> list[Stock]:
        return self.get_all_stocks(weights)[:n_top]

    def get_all_stocks(self, weights: dict[int, float]) -> list[Stock]:
        stocks = self._loader.load_stocks()
        counter = defaultdict(float)
        for stock in stocks:
            if stock.fund_id in weights:
                stock.part *= weights[stock.fund_id]
            else:
                stock.part = 0
        sum_of_stocks = sum(stock.part for stock in stocks)
        for stock in stocks:
            counter[stock.name] += stock.part / sum_of_stocks
        return sorted(counter.items(), key=lambda item: item[1], reverse=True)


stocks_statistics = StocksStatistics()
print(stocks_statistics.get_top_stocks(
    weights={5: 0.33, 6: 0.33, 7: 0.34},
    n_top=5,
))
