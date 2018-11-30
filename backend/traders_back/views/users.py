from flask import session, request, jsonify, Blueprint, render_template, redirect, url_for, flash

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
            flash("Invalid User Credential")
            return render_template("login.html")
        
        return redirect(url_for('users.user_page', uid=ret['uid'], user=user))

    return render_template("login.html")

def get_account_info_help(uid):
    res = manage.get_user_accounts(uid)
    if res['status']:
        return res['accounts']
    return None

@users.route('/user_page')
def user_page():
    uid = request.args.get('uid')
    user = request.args.get('user')

    print('user_page')
    print('uid: ', uid)
    print('user: ', user)
    accounts = manage.get_user_accounts(uid)['accounts']

    return render_template('user_page.html', uid=uid, user=user, accounts=accounts)
    
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
       
@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('Create/index.html')

    req = utils.get_req_data()
    user = req['username']
    pswd = req['password']
    email = req['email']

    ret = manage.sign_up(email, user, pswd)

    if not ret['status']:
        flash("User name already taken")
        return render_template('Create/index.html')

    flash("Successfully created a new user")
    return redirect(url_for('users.user_login'))
    
@users.route('/script_login', methods=['GET', 'POST'])
def script_login():
    if request.method == 'POST':
        req = utils.get_req_data()
        user = req['userName']
        pswd = req['passWord']
        ret = manage.sign_in(user, pswd)

        return jsonify(ret)
