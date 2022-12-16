from evaluating_funds.evaluating import get_finds_info
from db.db import DBLoader
from pprint import pprint

# from evaluating_funds.evaluating import evaluate_funds_rating, get_finds_info
#
# funds = get_finds_info()
# funds = evaluate_funds_rating(funds)
#
# pprint(funds)

loader = DBLoader()
pprint(loader.load_categories_of_funds())
