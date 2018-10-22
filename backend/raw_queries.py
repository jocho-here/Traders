# Place to keep the raw queries

## Table creating raw queries
create_users = """
               CREATE TABLE Users (
                   id INT NOT NULL AUTO_INCREMENT,
                   email VARCHAR(256) NOT NULL UNIQUE,
                   username VARCHAR(256) NOT NULL UNIQUE,
                   password VARCHAR(256) NOT NULL,
                   last_login DATETIME NOT NULL,
                   PRIMARY KEY (id)
               )
               """

create_accounts = """
                  CREATE TABLE Accounts (
                  id INT NOT NULL UNIQUE,
                  user_id INT NOT NULL,
                  account_name VARCHAR(256) NOT NULL,
                  open_date DATETIME NOT NULL,
                  close_date DATETIME,
                  PRIMARY KEY (user_id, account_name),
                  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
                  )
                  """

def create_positions():
    sql = """
          CREATE TABLE Positions (
              id INT NOT NULL UNIQUE,
              account_id INT NOT NULL,
              open_rate_id INT NOT NULL,
              close_rate_id INT,
              position_type VARCHAR(256) NOT NULL,
              position_status VARCHAR(256) NOT NULL,
              volume FLOAT NOT NULL,
              PRIMARY KEY (account_id, id),
              FOREIGN KEY (account_id)
                  REFERENCES Accounts(id)
                  ON DELETE CASCADE,
              FOREIGN KEY (open_rate_id)
                  REFERENCES ExchangeRates(id),
              FOREIGN KEY (close_rate_id)
                  REFERENCES ExchangeRates(id)
          )
          """
    return sql

def create_exchangerates():
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
    return sql

## User related raw queries
def insert_new_user():
    sql = """
          INSERT INTO Users (email, username, password, last_login)
                  VALUES (%s, %s, %s, %s)
          """
    return sql

def get_user_id_from_email():
    sql = """
          SELECT id FROM Users WHERE email = %s
          """
    return sql

def get_all_users():
    sql = """
          SELECT * FROM Users
          """
    return sql


## Account related raw queries
#def 
