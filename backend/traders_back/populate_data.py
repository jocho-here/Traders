import traders_back.manage as manage
import traders_back.utils as utils
from datetime import datetime

emails = [
            'mcho1@illinois.edu',
            'mcho12@illinois.edu',
            'mcho123@illinois.edu',
            'mcho1234@illinois.edu'
         ]
usernames = [
                'jo1',
                'jo2',
                'jo3',
                'jo4'
            ]
account_names = [
                    'account1',
                    'account2',
                    'account3',
                    'account4',
                    'account5'
                ]
exchange_rates =\
[
    {
        'currency_from':'gbp',
        'currency_to':'usd',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-01 11:11:11'
    },
    {
        'currency_to':'gbp',
        'currency_from':'usd',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-02 11:11:11'
    },
    {
        'currency_from':'gbp',
        'currency_to':'usd',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-03 11:11:11'
    },
    {
        'currency_to':'gbp',
        'currency_from':'usd',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-04 11:11:11'
    },
    {
        'currency_from':'usd',
        'currency_to':'gbp',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-05 11:11:11'
    },
    {
        'currency_to':'usd',
        'currency_from':'gbp',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-06 11:11:11'
    },
    {
        'currency_to':'usd',
        'currency_from':'gbp',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-07 11:11:11'
    },
    {
        'currency_to':'usd',
        'currency_from':'gbp',
        'bid':13.8,
        'ask':13.8,
        'time':'2018-01-08 11:11:11'
    }
]

user_ids = []
account_ids = {} # Key: user_id, Value: list of account_id's
exchange_rate_ids = []
position_ids = {}

# Initializing DB
utils.reset_db()

# Create users
for i in range(len(emails)):
    result = manage.sign_up(emails[i], usernames[i], usernames[i])
    user_ids.append(result['user_id'])

# Create accounts
for user_id in user_ids:
    account_ids[user_id] = []
    position_ids[user_id] = {}

    for account_name in account_names:
        result = manage.create_account(user_id, account_name)
        account_ids[user_id].append(result['account_id'])
        position_ids[user_id][result['account_id']] = []

# Create exchange rates
for rate in exchange_rates:
    result = manage.add_exchange_rate(rate['currency_from'], rate['currency_to'], rate['bid'], rate['ask'], rate['time'])
    exchange_rate_ids.append(result['rate_id'])

# Create positions
for user_id in account_ids:
    for account_id in account_ids[user_id]:
        result = manage.create_position(account_id, 'gbp', 'usd', '2018-01-01 11:11:11', 'long', 111.1)
        position_ids[user_id][account_id].append(result['position_id'])
