from flask import request

import traders_back.utils as utils
import traders_back.manage as manage

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST', 'DELETE', 'GET'])
def user_manipulation():
    rtn_val = {}
    req = utils.get_req_data()

    if request.method == 'POST':
        # New user sign up
        if 'email' in req and 'username' in req and 'password' in req:
            result = manage.sign_up(req['email'], req['username'], req['password'])
            rtn_val['status'] = True
            rtn_val['message'] = "Successfully signed up"
            rtn_val['email'] = email
        else:
            rtn_val['status'] = False
            rtn_val['message'] = "Request is missing either email, username, or password"
    elif request.method == 'GET':
        # This is just for testing purpose
        rtn_val = manage.get_all_users()
        rtn_val['status'] = True
    elif request.method == 'DELETE':
        # Delete a user
        if 'email' in req and 'password' in req:
            result = manage.delete_user(req['email'], req['password'])
            ####################################################
            

    return rtn_val
