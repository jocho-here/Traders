from flask import request

import traders_back.utils as utils
import traders_back.manage as manage

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST', 'DELETE', 'GET'])
def user_manipulation():
    rtn_val = {}
    req = utils.get_req_data()

    # New user sign up
    if request.method == 'POST':
        if 'email' in req and 'username' in req and 'password' in req:
            rtn_val = manage.sign_up(req['email'], req['username'], req['password'])
            rtn_val['status'] = True
            rtn_val['message'] = "Successfully signed up"
            rtn_val['email'] = email
        else:
            rtn_val['status'] = False
            rtn_val['message'] = "Request is missing either email, username, or password"
    elif request.method == 'GET':
        print('GET')
        # Open this up just for testing
    elif request.method == 'DELETE':
        print('DELETE')

    return rtn_val
