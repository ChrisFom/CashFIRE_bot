import numpy as np
from sklearn.linear_model import LogisticRegression
from pathlib import Path
import pickle

from data_source.data_loaders import DBLoader
from models.models import Fund


def get_funds_info() -> list[Fund]:
    loader = DBLoader()
    funds_info = loader.load_funds()

    return funds_info


class RiskModel:
    def __init__(self):
        self.model = LogisticRegression()

    def fit(self, train_data: np.ndarray, train_target: np.ndarray):
        self.model.fit(train_data, train_target)
        self._save_model()

    def predict(self, test_data: np.ndarray) -> float:
        return self.model.predict_proba(test_data.reshape(1, -1))[0, 1]

    def _save_model(self):
        save_path = Path('../pretrained_models').absolute() / 'risk_model.pkl'
        with open(save_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, model_path: Path):
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)


def generate_synthetic_data() -> tuple[np.ndarray, np.ndarray]:
    """ """
    features = ['price', 'profit', 'volatility', 'positive_years', 'negative_years']

    funds = get_funds_info()
    features_list = list()
    target_list = list()
    for fund in funds:
        fund.default_count_risk_level()
        profit = fund.average_profit
        price = fund.price
        volatility = fund.average_volatility
        positive_years = fund.positive_years
        negative_years = fund.negative_years
        features_list.append([profit,
                              price,
                              volatility,
                              positive_years,
                              negative_years])

        target = int(fund.risk_level > 0.08)
        target_list.append([target])
    features_data = np.array(features_list)
    features_data = np.nan_to_num(features_data)
    target_data = np.array(target_list)

    return features_data, target_data


def fit_model() -> RiskModel:
    x, y = generate_synthetic_data()
    model = RiskModel()

    model.fit(x, y)
    return model
