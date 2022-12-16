from collections import defaultdict

from data_source.data_loaders import DBLoader
from models.models import Stock


class StocksStatistics:
    _loader = DBLoader()

    def get_top_stocks(self, weights: dict[int, float], n_top: int):
        stocks = self.get_all_stocks(weights)[:n_top]
        stocks = [list(i) for i in stocks]
        nice_stocks = []
        for i in stocks:
            nice_stocks.append(f'{i[0]} - {round(i[1], 3)}')
        nice_stock_string = "\n".join(nice_stocks)
        return nice_stock_string

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


if __name__ == '__main__':
    stocks_statistics = StocksStatistics()
    print(stocks_statistics.get_top_stocks(
        weights={5: 0.33, 6: 0.33, 7: 0.34},
        n_top=10,
    ))
