from flask import request, jsonify, Blueprint

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
    ret['users'] = data
    return jsonify(ret)
        
@users.route('/signin', methods=['POST'])
def user_signin():
    req = utils.get_req_data()
    email = req['email']
    pswd = req['password']
    query = '''SELECT U.id uid, A.id accid FROM Users U LEFT JOIN Accounts A ON
            U.id=A.user_id WHERE U.email=%s AND U.password=%s
            '''
    ret = utils.getter_db(query, (email, pswd))
    accounts = ret.pop('result')
    if len(accounts) == 0:
        ret['status'] = False
        ret['message'] = 'Sign in authentication failed. Please check email or password'
        return jsonify(ret)
    ret['user_id'] = accounts[0]['uid']
    accounts = [i['accid'] for i in accounts]
    ret['account_ids'] = accounts
    query = 'UPDATE Users SET last_login="%s" WHERE id=%d' %(utils.get_date_time(), ret['user_id'])
    utils.setter_db(query)
    return jsonify(ret)
