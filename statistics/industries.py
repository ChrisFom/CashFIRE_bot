from collections import defaultdict

from data_source.data_loaders import DBLoader
from utils.industries_mapping import mapping


class IndustriesStatistics:

    _loader = DBLoader()

    def get_top_industries(self, weights: dict[int, float], n_top: int):
        industries = self.get_all_industries(weights)[:n_top]
        industries = [list(i) for i in industries]
        nice_industries = []
        for i in industries:
            nice_industries.append(f'{mapping[i[0]]} - {round(100*i[1], 2)}%')
        nice_industries_string = "\n".join(nice_industries)
        return nice_industries_string

    def get_all_industries(self, weights: dict[int, float]):
        categories = self._loader.load_raw_categories()

        counter = defaultdict(float)
        for id, cats in categories.items():
            for name, part in cats.items():
                if id in weights:
                    counter[name] += weights[id]*part

        return sorted(counter.items(), key=lambda item: item[1], reverse=True)


if __name__ == '__main__':
    industries = IndustriesStatistics()
    print(industries.get_top_industries(
        {
            1: 0.16687770921227246,
            16: 0.15233477048199173,
            17: 0.23478232819024963,
            18: 0.18209965876881642,
            19: 0.19605903400497468,
        },
        3
    ))
