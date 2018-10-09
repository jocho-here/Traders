from flask import jsonify, Blueprint


# This is where we create API endpoints for interacting with frontend

some_blueprint = Blueprint('some_blueprint', __name__)

@some_blueprint.route('/somemethod')
def temp_function():
    print("temp_function")
    return jsonify("temp_function")
