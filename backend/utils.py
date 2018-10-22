from flask import request
import re, json
import pymysql.cursors


# This is where utility functions reside
# For example, checking whether tables are there and resetting them and etc.
tables = ['Positions', 'Accounts', 'Users', 'ExchangeRates']

def setter_db(sql):
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def getter_db(sql):
    conn = get_conn()
    result = None

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
    except Exception as e:
        print(e)
        result = None
    finally:
        conn.close()

    return result

def create_users_table():
    sql = """
          CREATE TABLE Users (
              email VARCHAR(256) NOT NULL,
              username VARCHAR(256) NOT NULL UNIQUE,
              password VARCHAR(256) NOT NULL,
              last_login DATETIME NOT NULL,
              PRIMARY KEY (email)
          )
          """
    setter_db(sql)
    
def create_accounts_table():
    sql = """
          CREATE TABLE Accounts (
              account_name VARCHAR(256) NOT NULL,
              email VARCHAR(256) NOT NULL,
              open_date DATETIME NOT NULL,
              close_date DATETIME,
              PRIMARY KEY (account_name, email),
              FOREIGN KEY (email) REFERENCES Users(email) ON DELETE CASCADE
          )
          """
    setter_db(sql)

def create_exchangerates_table():
    sql = """
          CREATE TABLE ExchangeRates (
              id INT NOT NULL AUTO_INCREMENT,
              currency_from VARCHAR(128) NOT NULL,
              currency_to VARCHAR(128) NOT NULL,
              bid FLOAT NOT NULL,
              ask FLOAT NOT NULL,
              time TIMESTAMP NOT NULL,
              PRIMARY KEY (id)
          )
          """
    setter_db(sql)

def create_positions_table():
    sql = """
          CREATE TABLE Positions (
              account_name VARCHAR(256) NOT NULL,
              position_id INT NOT NULL,
              open_rate_id INT NOT NULL,
              close_rate_id INT,
              position_type VARCHAR(256) NOT NULL,
              position_status VARCHAR(256) NOT NULL,
              volume FLOAT NOT NULL,
              PRIMARY KEY (account_name, position_id),
              FOREIGN KEY (account_name)
                  REFERENCES Accounts(account_name)
                  ON DELETE CASCADE,
              FOREIGN KEY (open_rate_id)
                  REFERENCES ExchangeRates(id),
              FOREIGN KEY (close_rate_id)
                  REFERENCES ExchangeRates(id)
          )
          """
    setter_db(sql)

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


## DB related
# Getting the MySQL Connection
def get_conn():
    return pymysql.connect(host='localhost',
                           user='admin',
                           password='adminpw1',
                           db='tradersdb',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

# Creating tables if not found
def check_tables():
    sql = """
          SHOW TABLES
          """
    result = [x['Tables_in_tradersdb'] for x in getter_db(sql)]

    for table in tables:
        if table not in result:
            for table in tables:
                sql = """
                      DROP TABLE IF EXISTS {}
                      """.format(table)
                setter_db(sql)

            create_exchangerates_table()
            create_users_table()
            create_accounts_table()
            create_positions_table()
            break

    return result

# Creating new traders database if not existing
def create_new_database():
    print("create_new_database")

# DB health check
def db_checks():
    print("db_checks")
    #create_tables()

# Cleaning up database connections
def db_close():
    print("db_close")

# Totally resetting database
def reset_db():
    print("reset_db")
    #if not database_exists(get_db_url()):
    #    create_new_database()
    #
    #erase_tables()
    #create_tables()
