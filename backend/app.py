from flask import Flask

from views.some_blueprint import pages


# This is where we start our backend app
app = Flask(__name__)

# Blueprint registration
app.register_blueprint(pages)


if __name__ == '__main__':
    #db_checks()
    app.run(debug=True, host='localhost', port=8080)
    #db_close()
