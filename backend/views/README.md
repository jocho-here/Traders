# Traders API Documentation

- [User Management](#user-related)
- [Account Management](#account-related)
- [Position Management](#position-related)

## User Related

## Users Manipulation [/users]
### Sign up the new user [POST]

+ Request Body (application/json)

        {
            "email": "someone@email.com",
            "username": "someone",
            "password": "somepassword"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully signed up",
            "email": "someone@email.com",
            "user_id": 123
        }

### Delete a user [DELETE]

+ Request Body (application/json)

        {
            "email": "someone@email.com",
            "password": "somepassword"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully deleted a user",
            "deleted_user_email": "someone@email.com"
        }

### Get all users [GET]

This API endpoint exists just for testing.

+ Response 200 (application/json)

        {
            "status": true,
            "users": [
                {
                    "user_email": "someone@email.com",
                    "user_id": 123,
                    "accounts": [
                        {
                            "account_name": "someaccount1"
                        },
                        {
                            "account_name": "someaccount2"
                        },
                        {
                            "account_name": "someaccount3"
                        }
                    ]
                }
            ]
        }

## User Sign in [/signin]
### Sign in a user [POST]

+ Request Body (application/json)

        {
            "email": "someone@email.com",
            "password": "somepassword"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully signed in",
            "user_id": 123,
            "account_ids": [
                123,
                123,
                123
            ]
        }


## Account Related

## New Sub-account Creation [/new_account?uid=<INT>]

### Create a sub-account under a user [POST]

+ Request Body (application/json)

        {
            "account_name": "someaccountname"
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully created a new sub-account",
            "user_email": "someone@email.com",
            "account_name": "someaccountname",
            "account_id": 321
        }


## Sub-account [/{user_id}/{account_id}]

### Request account information [GET]

+ Response 200 (application/json)

        {
            "status": true,
            "user_email": "someone@email.com",
            "user_id": 123,
            "account_name": "someaccountname",
            "open_date": 2018-10-10 23:23:23,
            "positions": [
                ...
            ]
        }

### Delete account [DELETE]

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully delete the account",
            "deleted_account_name": "someaccountname",
            "close_date": 2018-10-10 24:24:24
        }


## Position Related

## Position Management [/{user_id}/{account_id}/positions]

### Get all positions [GET]
This API lets `from_date`, `to_date`, and `status` to be configured.  If you want to get positions
within specific dates, send request to `/{user_id}/{account_id}/positions/from/{from_date}/to/{to_date}`.
If you want to get positions within specific dates and with certain status (open or close), make a
request to `/{user_id}/{account_id}/positions/from/{from_date}/to/{to_date}/status/{status}`.  If you want to see
positions that are with certain status, make a request to `/{user_id}/{account_id}/positions/status/{status}`.

+ Response 200 (application/json)

        {
            "status": true,
            "positions": {
                "account_name": [
                    {
                        "position_id": 1,
                        "currency_from": "usd",
                        "currency_to": " "gbp",
                        "open_rate_id": 1,
                        "close_rate_id": null,
                        "position_type": "short",
                        "position_status": "open",
                        "volume": 123.3
                    },
                    {
                        "position_id": 2,
                        "currency_from": "usd",
                        "currency_to": "gbp",
                        "open_rate_id": 1,
                        "close_rate_id": 2,
                        "position_type": "long",
                        "position_status": "closed",
                        "volume": 123.3
                    }
                ]
            }
        }

### Create a new position [POST]

+ Request Body (application/json)

        {
            "currency_from": "usd",
            "currency_to": "gbp",
            "time": 2018-10-10 11:11:11,
            "position_type": "short",
            "volume": 123.3
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully created a new position",
            "position_id": 4
        }

or

        {
            "status": false,
            "message": "Failed to create a new position",
            "code": 100
        }
Code Representation  
- 100: Insufficient balance


## Individual Position [/{user_id}/{account_id}/{position_id}]
## Get the position information [GET]

+ Response 200 (application/json)

        {
            "status": true,
            "position": {
                "position_id": 2,
                "currency_from": "usd",
                "currency_to": "gbp",
                "open_rate_id": 1,
                "close_rate_id": null,
                "position_type": "long",
                "position_status": "open",
                "volume": 123.3
            }
        }

## Close the position [POST]

+ Request Body (application/json)

        {
            "close_time": 2018-10-10 11:11:11
        }

+ Response 200 (application/json)

        {
            "status": true,
            "message": "Successfully closed position"
        }
