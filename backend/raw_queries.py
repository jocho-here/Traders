# Place to keep the raw queries

create_users = """
               CREATE TABLE Users (
                   id INT NOT NULL,
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
create_positions = """
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
create_exchangerates = """
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
