from flask import request
import re, json, time
import pymysql.cursors

import traders_back.raw_queries as raw_queries


# This is where utility functions reside
# For example, checking whether tables are there and resetting them and etc.

tables = ['Positions', 'Accounts', 'Users', 'ExchangeRates']

ERR_ACCOUNT_ID = 'User with such account id does not exist'

# Return current time frame
def get_date_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def datetime_type_exchange(dt):
    if type(dt) is str:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(dt)

# Receive request data
def get_req_data():
    req = None

    if len(request.form) > 0:
        # Postman
        # request.data is empty with Postman
        print("Getting data from request.form")
        req = request.form
    elif len(request.data) > 0:
        # React
        # request.form is empty with react
        print("Getting data from request.data")
        req = json.loads(request.data.decode("utf-8"))

    return req


#### DB related
# Check if row exist, reutrn True of False based on select count
def check_exist_db(sql, data=None):
    conn = get_conn()
    try: 
        with conn.cursor() as cursor:
            cursor.execute(sql, data)
            if cursor.rowcount > 0:
                return True
    except:
        pass
    return False


# Any query that requires changes in the DB
def setter_db(sql, data=None):
    rtn_val = {'status':False, 'message':None}
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            if data != None:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
        conn.commit()
        rtn_val['last_insert_index'] = cursor.lastrowid
        rtn_val['status'] = True
    except Exception as e:
        print(e)
        rtn_val['message'] = str(e)
        conn.rollback()
    finally:
        conn.close()

    return rtn_val

# Any query that does not require any changes in the DB
def getter_db(sql, data=None):
    conn = get_conn()
    rtn_val = {'status':False}

    try:
        with conn.cursor() as cursor:
            if data != None:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)
            rtn_val['result'] = cursor.fetchall()
            rtn_val['status'] = True
    except Exception as e:
        print(e)
        rtn_val['message'] = str(e)
    finally:
        conn.close()

    return rtn_val

# Create Users table
def create_users_table():
    setter_db(raw_queries.create_users)
    
# Create Accounts table
def create_accounts_table():
    setter_db(raw_queries.create_accounts)

# Create ExchangeRates table
def create_exchangerates_table():
    setter_db(raw_queries.create_exchangerates)

# Create Positions table
def create_positions_table():
    setter_db(raw_queries.create_positions)

# Getting the MySQL Connection
def get_conn():
    return pymysql.connect(host='localhost',
                           user='admin',
                           password='adminpw1',
                           db='tradersdb',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


# feed some of data for testing, add more if needed
def fill_in_test_data():
    for q in raw_queries.feed_test_data:
        setter_db(q)

# Creating tables if not found
def check_tables():
    print("check tables")
    sql = """
          SHOW TABLES
          """
    result = [x['Tables_in_tradersdb'] for x in getter_db(sql)['result']]

    for table in tables:
        if table not in result:
            print("{} not in DB; resetting the whole DB")
            reset_db()
            fill_in_test_data()
            break

    return result

# Totally resetting database
def reset_db():
    print("reset_db")

    for table in tables:
        sql = """
              DROP TABLE IF EXISTS {}
              """.format(table)
        setter_db(sql)

    create_exchangerates_table()
    create_users_table()
    create_accounts_table()
    create_positions_table()
    
