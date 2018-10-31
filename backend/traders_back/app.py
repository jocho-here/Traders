from flask import Flask
from flask_cors import CORS

from utils import check_tables
from views.accounts import accounts
from views.users import users
from views.exchange_rates import exchange_rates
from views.positions import positions

# This is where we start our backend app
app = Flask(__name__)

# Blueprint registration
app.register_blueprint(accounts)
app.register_blueprint(users)
app.register_blueprint(exchange_rates)
app.register_blueprint(positions)

CORS(app=app)

if __name__ == '__main__':
    check_tables()
    app.run(debug=True, host='localhost', port=8080)
