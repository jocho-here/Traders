from flask import jsonify, Blueprint, render_template, request, redirect, url_for
import traders_back.utils as utils

accounts = Blueprint('accounts', __name__)


'''
@pages.route('/profile', methods=['GET', 'POST'])
def user_profile():
	if request.method == 'GET':
		print(request)
		uid = request.args.get('uid')
		if not uid:
			return "usage: </profile?uid=INT>"
		return render_template("user_index.html", logged="true") #Not sure if this is the right thing to do.. The line below was the original.
		return 'user_id: ' + str(uid)
	elif request.method == 'POST':
		info = request.form
		accID = info['account']
		return redirect(url_for('pages.user_account', accID=accID))
@pages.route('/account')
def user_account():
	accID = request.args.get('accID')
	if not accID:
		return "usage: </account?accID=INT"
	return render_template("user_account.html")
'''

@accounts.route('/account')
def account_apis():
    return "Accounts"
	
@accounts.route('/new_account', methods=['POST'])
def create_new_account():
    uid = int(request.args.get('uid'))
    name = utils.get_req_data()['account_name']
    query = '''Insert into Accounts (
        account_name, open_date, user_id) values (
        %s, %s, %s) ''' 
    ret = utils.setter_db(query, (name, utils.get_date_time(), uid))
    if not ret['status']:
        return jsonify(ret)
    query = 'SELECT email FROM Users WHERE id=%s'
    email = utils.getter_db(query, (uid))['result'][0]['email']
    ret['user_email'] = email
    ret['account_id'] = ret.pop('last_insert_index')
    return jsonify(ret)
    	
@accounts.route('/<int:uid>/<int:accid>', methods=['GET', 'DELETE'])
def sub_account(uid, accid):
    ret = {"status":False}
    if request.method == 'GET':
	    query = '''SELECT U.email, 
	            A.account_name, A.open_date, A.close_date
		        FROM Users U JOIN Accounts A ON U.id=A.user_id
		        WHERE U.id=%s AND A.id=%s'''
	    ret = utils.getter_db(query, (uid, accid))
	    info = ret.pop('result')
	    if len(info) == 0:
	        ret['status'] = False
	        ret['message'] = utils.ERR_ACCOUNT_ID
	        return jsonify(ret)
	    info = info[0]
	    if info['close_date']:
	        ret['message'] = 'Account has been closed'
	        return jsonify(ret)
	    ret['user_email'] = info['email']
	    ret['account_name'] = info['account_name']
	    ret['open_date'] = info['open_date']
	    ret['user_id'] = uid
	    return jsonify(ret)
    elif request.method == 'DELETE':
        query = '''SELECT account_name FROM Accounts 
	             WHERE id=%s AND user_id=%s'''
        ret = utils.getter_db(query, (accid, uid))
        data = ret.pop('result')
        if len(data) == 0:
            ret['status'] = False
            ret['message'] = utils.ERR_ACCOUNT_ID
            return jsonify(ret)
        ret['deleted_account_name'] = data[0]['account_name']      
        date = utils.get_date_time()
        ret['close_date'] = date
        query = 'UPDATE Accounts SET close_date=%s WHERE id=%s'
        utils.setter_db(query, (date, accid))
        return jsonify(ret)
	       
@accounts.route('/accounts')
def get_accounts():
    q = '''SELECt U.id, U.email, U.username, U.last_login, 
        A.id, A.available_equity, 
        A.account_name, A.open_date, A.close_Date 
        FROM Users U JOIN Accounts A on U.Id=A.USER_ID'''
    ret = utils.getter_db(q)
    return jsonify(ret)
    
    
