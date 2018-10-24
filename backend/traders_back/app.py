from flask import Flask
from flask_cors import CORS

from utils import check_tables
from views.accounts import accounts


# This is where we start our backend app
app = Flask(__name__)

# Blueprint registration
app.register_blueprint(accounts)

CORS(app=app)

if __name__ == '__main__':
    check_tables()
    app.run(debug=True, host='localhost', port=8080)
