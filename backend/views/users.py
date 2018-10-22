from flask import request

from traders_back_utils as utils

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST', 'DELETE', 'GET'])
def user_manipulation():
    rtn_val = {}
    req = utils.get_req_data()

    if request.method == 'POST':
        if 'email' in req and 'username' in req and 'password' in req:
        else:
            rtn_val['status'] = False
            rtn_val['message'] = "Request is missing either email, username, or password"
    elif request.method == 'GET':
    elif request.method == 'DELETE':
