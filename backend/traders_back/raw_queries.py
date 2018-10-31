# Place to keep the queries

## Table creating queries
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
    available_equity REAL NOT NULL,
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
    id INT NOT NULL AUTO_INCREMENT,
    account_id INT NOT NULL,
    open_rate_id INT NOT NULL,
    close_rate_id INT,
    position_type VARCHAR(256) NOT NULL,
    position_status VARCHAR(256) NOT NULL,
    volume FLOAT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id, account_id),
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


## User related queries

#check_user_existence =\
#"""
#SELECT *
#FROM Users
#WHERE email=%s OR username=%s 
#"""
insert_new_user =\
"""
INSERT INTO Users (email, username, password, last_login)
    VALUES (%s, %s, %s, %s)
"""

get_user_id_from_email =\
"""
SELECT id FROM Users WHERE email = %s
"""

get_user_info_from_id =\
"""
SELECT * FROM Users WHERE id = %s
"""
get_all_users =\
"""
SELECT * FROM Users
"""

delete_user =\
"""
DELETE FROM Users
WHERE email = %s AND password = %s
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

# Positions related queries
get_positions =\
"""
SELECT P.*
FROM Positions P, ExchangeRates E
WHERE P.account_id = %s AND E.id = P.open_rate_id
"""

create_new_position =\
"""
INSERT INTO Positions (account_id, open_rate_id, position_type, position_status, volume)
    VALUES (%s, %s, %s, %s, %s)
"""

get_position_from_id =\
"""
SELECT P.*
FROM Positions
WHERE id = %s
"""

close_position_with_id =\
"""
UPDATE Positions SET close_rate_id = %s WHERE id = %s
"""

# ExchangeRate realted queries
get_exchange_rate =\
"""
SELECT *
FROM ExchangeRates
"""


# Account related queries
create_account =\
"""
INSERT INTO Accounts(user_id, account_name, available_equity, open_date)
    VALUES(%s, %s, %s, %s)
"""

delete_account =\
"""
DELETE FROM Accounts
WHERE user_id = %s AND id = %s
"""

get_account_info_from_uid_accname =\
"""
SELECT *
FROM Accounts
WHERE user_id = %s AND account_name = %s
"""

get_account_info_from_uid_accid =\
"""
SELECT *
FROM Accounts
WHERE user_id = %s AND id = %s
"""

get_user_accounts =\
"""
SELECT *
FROM Accounts
WHERE user_id = %s
"""
