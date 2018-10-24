import pymysql.cursors
from datetime import datetime

from utils import setter_db, getter_db
import raw_queries

# This is where queries reside


def delete_user(email, password):
    rtn_val = {}
    
    if getter_db(raw_queries.signin(email, password))['status'] == True:
        setter_db(raw_queries.delete_user, (email,))
        ########################################################

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
