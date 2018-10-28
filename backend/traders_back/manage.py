import pymysql.cursors
from datetime import datetime

from utils import setter_db, getter_db
import raw_queries


def create_position(account_id, currency_from, currency_to, time, position_type, volume):
    rtn_val = {}
    result = get_exchange_rates(currency_from, currency_to, time)

    if result['status']:
        data = [account_id, result['exchange_rate']['id'], position_type, 'open', volume]
        result = setter_db(raw_queries.create_new_position, data=tuple(data))

        if result['status']:
            rtn_val['status'] = True
            rtn_val['message'] = "Successfully created a new position"
            rtn_val['position_id'] = result['last_insert_index']
        else:
            rtn_val = result
    else:
        rtn_val['status'] = False
        rtn_val['message'] = "Failed to create a new position; Could not find the exchange rate"
        
    return rtn_val

# TODO
#def get_exchange_rate_by_id(rate_id):
#    modified_qery = raw_queries.get_exchange_rate + '\nWHERE id = %s'

def get_exchange_rates(currency_from, currency_to, time=None):
    rtn_val = {}
    modified_query = raw_queries.get_exchange_rate + '\nWHERE currency_from = %s AND currency_to = %s'
    data = [currency_from, currency_to]

    if time:
        modified_query += ' AND time = %s'
        data.append(time)

    result = getter_db(modified_query, data=tuple(data))

    if result['status']:
        rtn_val['status'] = True
        rtn_val['currency_from'] = currency_from
        rtn_val['currency_to'] = currency_to
        rtn_val['exchange_rates'] = []

        for rate in result['result']:
            curr_rate = {}
            curr_rate['id'] = rate['id']
            curr_rate['bid'] = rate['bid']
            curr_rate['ask'] = rate['ask']
            curr_rate['time'] = rate['time']
            rtn_val['exchange_rates'].append(curr_rate)

        if time:
            rtn_val['exchange_rate'] = rtn_val.pop('exchange_rates')[0]
    else:
        rtn_val = result

    return rtn_val

def get_positions(account_id, from_date=None, to_date=None, status=None):
    rtn_val = {}
    modified_query = raw_queries.get_positions
    data = [account_id]

    if from_date and to_date:
        modified_query += ' AND E.time >= %s AND E.time <= %s'
        data.append(from_date)
        data.append(to_date)
    if status:
        modified_query += ' AND P.position_status = %s'
        data.append(status)

    result = getter_db(modified_query, data=tuple(data))

    if result['status']:
        rtn_val['status'] = True
        rtn_val['positions'] = []

        for pos in result['result']:
            curr_pos = {}
            curr_pos['id'] = pos['id']
            curr_pos['open_rate_id'] = pos['open_rate_id']
            curr_pos['close_rate_id'] = pos['close_rate_id']
            curr_pos['position_type'] = pos['position_type']
            curr_pos['position_status'] = pos['position_status']
            curr_pos['volume'] = pos['volume']
            rtn_val['positions'].append(curr_pos)
    else:
        rtn_val['status'] = False
        rtn_val['message'] = result['message']

    return rtn_val

# TODO
# Check whether account_id is associated with the user_id
#def check_account_id(user_id, account_id)

# TODO
def delete_user(email, password):
    rtn_val = {}

    return "Need to implement"

def sign_up(email, username, password):
    rtn_val = {}
    setter_db(raw_queries.insert_new_user, data = (email,
                                                   username,
                                                   password,
                                                   datetime.utcnow()))
    result = getter_db(raw_queries.get_user_id_from_email(), data=(email,))['result']
    rtn_val['user_id'] = result[0]['id']

    return rtn_val

def get_all_users():
    rtn_val = {'users': []}
    result = getter_db(raw_queries.get_all_users())['result']

    for user in result:
        curr_user = {}
        curr_user['email'] = user['email']
        curr_user['username'] = user['username']
        curr_user['user_id'] = user['id']
        curr_user['last_login'] = user['last_login']
        rtn_val['users'].append(curr_user)

    return rtn_val
