import pymysql.cursors
from datetime import datetime

from utils import setter_db, getter_db
import raw_queries

# This is where queries reside


def sign_up(email, username, password):
    rtn_val = {}
    setter_db(raw_queries.insert_new_user(email,
                                          username,
                                          password,
                                          datetime.utcnow()))

    result = getter_db(raw_queries.get_user_id_from_email(), data=(email,))
    rtn_val['user_id'] = result[0]['id']

    return rtn_val

def get_all_users():
    rtn_val = {}
    result = getter_db(raw_queries.get_all_users())

    for user in result:
        
