from flask import request, jsonify, Blueprint, render_template, redirect, url_for

import traders_back.utils as utils
import traders_back.manage as manage

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        req = utils.get_req_data()
        user = req['userName']
        pswd = req['passWord']
        ret = manage.sign_in(user, pswd)
        if not ret['status']:
            return render_template("login.html")
        return redirect('/user_page/%s'%ret['uid'])		

    return render_template("login.html")

def get_account_info_help(uid):
    res = manage.get_user_accounts(uid)
    if res['status']:
        return res['accounts']
    return None

@users.route('/user_page')
def user_page():
    uid = request.args.get('uid')
    acc = get_account_info_help(uid)
    return render_template('live_trading.html', uid=uid, account_info=acc)
    
@users.route('/user_page/<int:uid>')
def user_page_without_chart(uid):
    acc = get_account_info_help(uid)
    return render_template('Account/index.html', uid=uid, account_info=acc)

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
            rtn_val['email'] = req['email']
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
       
""" 
@users.route('/signin', methods=['POST'])
def user_signin():
    req = utils.get_req_data()
    email = req['email']
    pswd = req['password']
    return manage.sign_in(email, pswd)
    ret = manage.try_get_user_info(email, pswd)
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
"""  
    
@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
	if request.method == 'GET':
		return render_template('Create/index.html')
	req = utils.get_req_data()
	user = req['username']
	pswd = req['password']
	ret = manage.sign_up(user+'@test.com', user, pswd)
	if not ret['status']:
		return ret['message']
	return redirect(url_for('users.user_login'))
