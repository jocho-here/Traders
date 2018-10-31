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

def get_exchange_rate_by_id(rate_id):
    rtn_val = {}
    modified_qery = raw_queries.get_exchange_rate + '\nWHERE id = %s'

    result = getter_db(modified_query, data=(rate_id,))

    if result['status']:
        rtn_val['status'] = True
        rtn_val['exchange_rate'] = result['result'][0]
    else:
        rtn_val = result

    return rtn_val

def get_exchange_rates(currency_from, currency_to, from_time=None, to_time=None, time=None):
    rtn_val = {}
    modified_query = raw_queries.get_exchange_rate + '\nWHERE currency_from = %s AND currency_to = %s'
    data = [currency_from, currency_to]

    if time:
        modified_query += ' AND time = %s'
        data.append(time)
    elif from_time and to_time:
        modified_query += ' AND time >= %s AND time <= %s'
        data.append(from_time)
        data.append(to_time)

    result = getter_db(modified_query, data=tuple(data))
    print(result)

    if result['status']:
        rtn_val['status'] = True
        rtn_val['currency_from'] = currency_from
        rtn_val['currency_to'] = currency_to

        if from_time and to_time:
            rtn_val['from_time'] = from_time
            rtn_val['to_time'] = to_time

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

def close_position(position_id, close_rate_id):
    rtn_val = {}
    modified_query = raw_queries.get_exchange_rate
    close_rate = get_exchange_rate_by_id(close_rate_id)

    if close_rate['status']:
        position = get_position(position_id)['position']
        close_rate = close_rate['exchange_rate']
        open_rate = get_exchange_rate_by_id(position['open_rate_id'])['exchange_rate']

        if open_rate.time > close_rate.time:
            rtn_val['status'] = False
            rtn_val['message'] = "Closing exchange rate is earlier than the opening exchange rate"
        else:
            result = setter_db(raw_queries.close_position_with_id, (close_rate_id, position_id))

            if result['status']:
                rtn_val['status']
                rtn_val['message'] = "Successfully closed position"
            else:
                rtn_val = result
    else:
        rtn_val['status'] = False
        rtn_val['message'] = "Exchange rate with the given close_rate_id does not exist"

    return rtn_val

def get_position(position_id):
    rtn_val = {}

    result = getter_db(raw_queries.get_position_from_id, data=(position_id,))

    if result['status']:
        rtn_val['status'] = True
        rtn_val['position'] = {}
        rtn_val['position']['id'] = position_id
        rtn_val['position']['open_rate_id'] = result['result']['open_rate_id']
        rtn_val['position']['close_rate_id'] = result['result']['close_rate_id']
        rtn_val['position']['position_type'] = result['result']['position_type']
        rtn_val['position']['position_status'] = result['result']['position_status']
        rtn_val['position']['volume'] = result['result']['volume']
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
