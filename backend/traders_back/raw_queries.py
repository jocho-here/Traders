# Place to keep the raw queries

## Table creating raw queries
create_users =\
"""
CREATE TABLE Users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(256) NOT NULL UNIQUE,
    username VARCHAR(256) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL,
    last_login DATETIME NOT NULL,
    PRIMARY KEY (id)
)
"""

create_accounts =\
"""
CREATE TABLE Accounts (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    account_name VARCHAR(256) NOT NULL,
    open_date DATETIME NOT NULL,
    close_date DATETIME,
    PRIMARY KEY (id),
    UNIQUE (user_id, account_name),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
)
"""

create_positions =\
"""
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
        REFERENCES ExchangeRates(id)
        ON DELETE CASCADE,
    FOREIGN KEY (close_rate_id)
        REFERENCES ExchangeRates(id)
        ON DELETE CASCADE
)
"""

create_exchangerates =\
"""
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


## User related raw queries
insert_new_user =\
"""
INSERT INTO Users (email, username, password, last_login)
    VALUES (%s, %s, %s, %s)
"""

get_user_id_from_email =\
"""
SELECT id FROM Users WHERE email = %s
"""

get_all_users =\
"""
SELECT * FROM Users
"""

delete_user =\
"""
DELETE FROM Users
WHERE email = %s
"""

feed_test_data = [
"""
INSERT INTO Users (
email, username, password, last_login) values (
'root@test.com', 'root', '1234', '2018-10-10 11:11:11')
""",
"""
INSERT INTO Accounts (
user_id, account_name, open_date) values (
1, 'root_account', '2018-10-10 11:11:11')
"""
]

## Account related raw queries
#def 
