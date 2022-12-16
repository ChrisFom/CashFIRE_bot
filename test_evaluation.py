from evaluating_funds.evaluating import get_finds_info
from pprint import pprint
from collections import OrderedDict

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# funds_info = get_finds_info()

from evaluating_funds.evaluating import evaluate_funds_rating, get_finds_info

funds = get_finds_info()
funds = evaluate_funds_rating(funds)
sorted_funds = sorted(funds.items(), key=lambda k: k[1]['rating'], reverse=True)

pprint(sorted_funds[:5])
