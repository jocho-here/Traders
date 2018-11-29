from flask import Flask
from flask_cors import CORS

from utils import check_tables
from views.accounts import accounts
from views.users import users
from views.exchange_rates import exchange_rates
from views.positions import positions
from views.model import model
from views.chart import chart

import os
# This is where we start our backend app
template_dir = os.path.abspath('../templates')
static_dir = os.path.abspath('../static')
app = Flask(__name__, 
    template_folder=template_dir,
    static_folder=static_dir
    )
app.secret_key = b'somesecret'


# Blueprint registration
app.register_blueprint(accounts)
app.register_blueprint(users)
app.register_blueprint(exchange_rates)
app.register_blueprint(positions)
app.register_blueprint(model)
app.register_blueprint(chart)

CORS(app=app)

if __name__ == '__main__':
    check_tables()
    app.run(debug=True, host='localhost', port=8080)
