import pymysql.cursors
from datetime import datetime


import traders_back.utils as utils
from traders_back.utils import setter_db, getter_db
import traders_back.raw_queries as raw_queries





def get_exchange_rate_by_id(rate_id):
    rtn_val = {}
    modified_query = raw_queries.get_exchange_rate + '\nWHERE id = %s'

    result = getter_db(modified_query, data=(rate_id,))

    if result['status'] and len(result['result']) > 0:
        rtn_val['status'] = True
        rtn_val['exchange_rate'] = result['result'][0]
    else:
        rtn_val = result

    return rtn_val

def add_exchange_rate(currency_from, currency_to, bid, ask, time):
    rtn_val = {'status': False}
    result = setter_db(raw_queries.add_exchange_rate, data = (currency_from, currency_to, bid, ask, time))

    if result['status']:
        rtn_val['status'] = True
        rtn_val['rate_id'] = result['last_insert_index']
    else:
        rtn_val['message'] = result['message']
        rtn_val = result
    return rtn_val
    
def get_exchange_rates(currency_from, currency_to, from_time=None, to_time=None, time=None):
    rtn_val = {}
    
    data = [currency_from, currency_to]

    if time:
        modified_query = raw_queries.get_nearest_exchange_rate
        data.append(time)
    elif from_time and to_time:
        modified_query = raw_queries.get_exchange_rate + '\nWHERE currency_from = %s AND currency_to = %s'
        modified_query += ' AND time >= %s AND time <= %s'
        data.append(from_time)
        data.append(to_time)

    result = getter_db(modified_query, data=tuple(data))
    if result['status'] and len(result['result']) > 0:
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
        rtn_val['status'] = False
        rtn_val['message'] = "Could not find the given exchange rate"

    return rtn_val
#
#def convert_to_USD(volume, currency, time):
#    """Converts a currency to USD using the most recent exchange rate to 'time'"""
    
def get_position(position_id):
    rtn_val = {}

    result = getter_db(raw_queries.get_position_from_id, data=(position_id,))
    
    if result['status'] and len(result['result']) > 0:
        rtn_val['status'] = True
        rtn_val['position'] = {}
        rtn_val['position']['id'] = position_id
        rtn_val['position']['account_id'] = result['result'][0]['account_id']
        rtn_val['position']['open_rate_id'] = result['result'][0]['open_rate_id']
        rtn_val['position']['close_rate_id'] = result['result'][0]['close_rate_id']
        rtn_val['position']['position_type'] = result['result'][0]['position_type']
        rtn_val['position']['position_status'] = result['result'][0]['position_status']
        rtn_val['position']['volume'] = result['result'][0]['volume']
        rtn_val['position']['value'] = 12345 #TODO UPDATE VALUE
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

    if result['status'] and len(result['result']) > 0:
        rtn_val['status'] = True
        rtn_val['positions'] = []

        for pos in result['result']:
            curr_pos = {}
            open_rate = get_exchange_rate_by_id(pos['open_rate_id'])['exchange_rate']
            curr_pos['id'] = pos['id']
            curr_pos['account_id'] = pos['account_id']
            curr_pos['currency_from'] = open_rate['currency_from']
            curr_pos['currency_to'] = open_rate['currency_to']
            curr_pos['open_rate_id'] = pos['open_rate_id']
            curr_pos['open_rate_time'] = open_rate['time']
            curr_pos['close_rate_id'] = pos['close_rate_id']

            if pos['close_rate_id'] != None:
                curr_pos['close_rate_time'] = get_exchange_rate_by_id(pos['close_rate_id'])['exchange_rate']['time']
            else:
                curr_pos['close_rate_time'] = None

            curr_pos['position_type'] = pos['position_type']
            curr_pos['position_status'] = pos['position_status']
            curr_pos['volume'] = pos['volume']
            curr_pos["value"] = 11234 #TODO SET TO BE CURRENT VAL
            rtn_val['positions'].append(curr_pos)
    else:
        rtn_val['status'] = False

    return rtn_val  
    
def create_position(account_id, currency_from, currency_to, time, position_type, volume):
    rtn_val = {}
    accinfo = get_account_info(account_id)["account_info"]
    available_equity = accinfo["available_equity"]
    
    result = get_exchange_rates(currency_from, currency_to, time=time)
    total_cost = volume*(1/result["exchange_rate"]["bid"])
    if currency_from != "USD":
        conversion_result = get_exchange_rates("USD", currency_from, time=time)
        total_cost  = total_cost*(1/conversion_result["exchange_rate"]["bid"])
    if total_cost > available_equity:
        rtn_val['status'] = False
        rtn_val['message'] = "Failed to create a new position; Not enough available equity."
        rtn_val['code'] = 100
	
    elif result['status']:
        data = [account_id, result['exchange_rate']['id'], position_type, 'open', volume]
        update_equity_status = setter_db(raw_queries.update_equity, data=(-total_cost, account_id))
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
        rtn_val['code'] = 200
        
    return rtn_val

def close_position(position_id, close_rate_time):
    rtn_val = {}
    open_info = getter_db(raw_queries.get_open_rate_info_with_id, data=(position_id,))["result"][0]
    close_rate = get_exchange_rates(open_info['currency_from'], open_info['currency_to'], time=close_rate_time)
    if close_rate['status']:
        
        close_rate = close_rate['exchange_rate']

        if type(open_info['time']) is str:
            open_info['time'] = utils.str_to_datetime(open_info['time'])

        if type(close_rate['time']) is str:
            close_rate['time'] = utils.str_to_datetime(close_rate['time'])
        
        if open_info['time'] > close_rate['time']:
            rtn_val['status'] = False
            rtn_val['message'] = "Closing exchange rate is earlier than the opening exchange rate"
        else:
            pos_info = get_position(position_id)['position']
            account_id = pos_info["account_id"]
            volume = pos_info["volume"]
            total_cost = volume*close_rate["ask"]
            if open_info["currency_from"] != "USD":
                conversion_result = get_exchange_rates("USD", open_info['currency_from'], time=close_rate_time)
                total_cost = total_cost*conversion_result["ask"]
            update_equity_status = setter_db(raw_queries.update_equity, data=(total_cost, account_id))
            result = setter_db(raw_queries.close_position_with_id, (close_rate['id'], "closed", position_id))

            if result['status']:
                rtn_val['status'] = True
                rtn_val['message'] = "Successfully closed position"
            else:
                rtn_val['status'] = False
                rtn_val['message'] = "Could not close position, see result for details"
                rtn_val['result'] = result
    else:
        rtn_val['status'] = False
        rtn_val['message'] = "Exchange rate with the given close_rate_time does not exist"

    return rtn_val



# TODO
# Check whether account_id is associated with the user_id
#def check_account_id(user_id, account_id)

def create_account(uid, acc_name, equity=100000):
    rtn_val = {}
    result = setter_db(raw_queries.create_account, data = (acc_name, utils.get_date_time(), uid, equity))
    if result['status']:
        rtn_val['status'] = True
    else:
        rtn_val['status'] = False
        rtn_val['message'] = result['message']
        return rtn_val
    
    acc_id = getter_db(raw_queries.get_account_info_from_uid_accname,
                                data=(uid,
                                      acc_name))['result'][0]['id']
    rtn_val['account_id'] = acc_id
    return rtn_val
    

def get_account_info(acc_id):
    rtn_val = {}
    result = getter_db(raw_queries.get_account_info_from_accid, data=(acc_id))
    
    if not result['status']:
        rtn_val['status'] = False
        rtn_val['message'] = result['message']
        return rtn_val
    elif len(result['result']) == 0:
        rtn_val['status'] = False
        rtn_val['message'] = "User_id Account_id pair not in DB"
        return rtn_val
    else:
        rtn_val['status'] = True
        
    acc_info = result['result'][0]
    acc_info["account_id"] = acc_info["id"]
    acc_info["account_value"] = 12345
    acc_info.pop('id', None)
    rtn_val["account_info"] = acc_info
        
    return rtn_val


def delete_account(acc_id):
    rtn_val = {}
    del_status = setter_db(raw_queries.delete_account, data=(acc_id))
    
    if not del_status['status']:
        rtn_val['status'] = False
        rtn_val['message'] = del_status['message']
    else:
        rtn_val['status'] = True
    return rtn_val    

def get_user_accounts(uid):
    rtn_val = {}
    result = getter_db(raw_queries.get_user_accounts, data=(uid))
    if result['status'] and len(result['result']) > 0:
        rtn_val['status'] = True
    else:
        rtn_val['status'] = False
        rtn_val['message'] = "Could not find the user with the user id"
        return rtn_val
    
    rtn_val["account_ids"] = []
    accounts = result['result']
    for account in accounts:
        account["account_id"] = account["id"]
        account.pop("id", None)
        rtn_val["accounts"].append(account)
    return rtn_val
        
    
# USER functions

def delete_user(email, password):
    rtn_val = {}
    result = setter_db(raw_queries.delete_user, data = (email, password))

    if result['status']:
        rtn_val['status'] = True
        rtn_val['message'] = "Successfully deleted a user"
        return rtn_val
    else:
        rtn_val['status'] = False
        rtn_val['message'] = result['message']
        return rtn_val

def sign_up(email, username, password):
    rtn_val = {}
   
    set_status = setter_db(raw_queries.insert_new_user, data = (email,
                                                   username,
                                                   password,
                                                   datetime.utcnow()))
    if not set_status['status']:
        rtn_val['status'] = False
        rtn_val['message'] = set_status['message']
        return rtn_val
    else:
        rtn_val['status'] = True
    result = getter_db(raw_queries.get_user_id_from_email, data=(email,))['result']
    rtn_val['user_id'] = result[0]['id']
    rtn_val['message'] = "Successfully signed up"

    return rtn_val

def get_all_users():
    rtn_val = {"status": True, 'users': []}
    result = getter_db(raw_queries.get_all_users)['result']

    for user in result:
        curr_user = {}
        curr_user['email'] = user['email']
        curr_user['username'] = user['username']
        curr_user['user_id'] = user['id']
        curr_user['last_login'] = user['last_login']
        rtn_val['users'].append(curr_user)

    return rtn_val

def get_user_info(uid):
    rtn_val = {}
    get_status = getter_db(raw_queries.get_all_users)
    if not get_status['status']:
        rtn_val['status'] = False
        rtn_val['message'] = get_status['message']
        return rtn_val
    elif len(get_status['result']) == 0:
        rtn_val['status'] = False
        rtn_val['message'] = "User ID not in DB"
        return rtn_val
    else:
        rtn_val['status'] = True
    rtn_val['user'] = get_status['result'][0]
    
    return rtn_val

