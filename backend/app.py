from flask import Flask
from flask_cors import CORS

from views.some_blueprint import some_blueprint


# This is where we start our backend app
app = Flask(__name__)

# Blueprint registration
app.register_blueprint(some_blueprint)

CORS(app=app)

if __name__ == '__main__':
    #db_checks()
    app.run(debug=True, host='0.0.0.0', port=8000)
    #db_close()
