import traders_back.manage as manage
import traders_back.utils as utils
from datetime import datetime, timedelta
import time, random


utils.setter_db('DELETE FROM ExchangeRates')

t = datetime.strptime('Nov 1 2018  8:30AM', '%b %d %Y %I:%M%p')
for i in range(3600):
	bid = random.uniform(1, 2)
	q = '''INSERT INTO ExchangeRates (
			currency_from, currency_to, bid, ask, time) values (
			"usd", "gbp", {0:.2f}, {1:.2f}, %s)
		'''.format(bid, bid)
	utils.setter_db(q, [t])
	t += timedelta(seconds=1)
