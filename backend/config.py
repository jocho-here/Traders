import os


# DB related
def get_db_url():
    if 'MYSQL_HOST' not in os.environ:
        print("Please set an environment variable MYSQL_HOST")
        exit(1)

    if 'MYSQL_PORT' not in os.environ:
        print("Please set an environment variable MYSQL_HOST")
        exit(1)

    db_host = os.environ['MYSQL_HOST']
    db_port = os.environ['MYSQL_PORT']

    return "mysql+pymysql://admin:adminpw1@{}:{}/tradersdb".format(db_host, db_port)
