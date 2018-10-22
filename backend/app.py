from flask import Flask

from utils import check_tables
from views.accounts import pages


# This is where we start our backend app
app = Flask(__name__)

# Blueprint registration
app.register_blueprint(pages)


if __name__ == '__main__':
    check_tables()
    app.run(debug=True, host='localhost', port=8080)
