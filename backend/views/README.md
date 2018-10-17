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


## Account Related

## New Sub-account Creation [/{user_id}/new_account]

### Create a sub-account under a user [POST]

+ Request Body (application/json)

		{
			"account_name": "someaccountname"
		}

+ Response (application/json)

		{
			"status": true,
			"message": "Successfully created a new sub-account",
			"user_email": "someone@email.com",
			"account_name": "someaccountname",
			"account_id": 321
		}


## Sub-account [/{user_id}/{account_id}]

### Request account information [GET]

+ Response (application/json)

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

+ Response (application/json)

		{
			"status": true,
			"message": "Successfully delete the account",
			"deleted_account_name": "someaccountname",
			"close_date": 2018-10-10 24:24:24
		}


## Position Management [/{user_id}/{account_id}/position]
