from flask import request, jsonify

import traders_back.utils as utils
import traders_back.manage as manage

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST', 'DELETE', 'GET'])
def user_manipulation():
    rtn_val = {'status':False}
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
            return jsonify(rtn_val)
    elif request.method == 'GET':
        uid = request.args.get('uid')
        return get_user_info(uid)
    elif request.method == 'DELETE':
        email = req['email']
        uid = req['uid']
        query = 'DELETE FROM Users WHERE id=%d AND email=%s'
        rtn_val = utils.setter_db(query, (uid, email))
        rtn_val.pop('last_insert_index')
        rtn_val['deleted_user_email'] = email
        return jsonify(rtn_val)

    
def get_user_info(uid):
    query = 'SELECT email, username, id, last_login From Users'
    if uid:
        query += ' WHERE id=%d' %int(uid)
    ret = utils.getter_db(query)
    data = ret.pop('result')
    ret['users'] = []
    for e in data:
        user = {}
        user['email'] = data[0]
        user['username'] = data[1]
        user['user_id'] = data[2]
        user['last_login'] = data[3]
        ret['users'].append(user)
    return jsonify(ret)
        
        
        
        
