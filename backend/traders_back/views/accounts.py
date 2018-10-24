from flask import jsonify, Blueprint, render_template, request, redirect, url_for
import traders_back.utils as utils

accounts = Blueprint('accounts', __name__)

'''
@pages.route('/login', methods=['GET', 'POST'])
def user_login():
	if request.method == 'POST':
		info = request.form
		if not all(k in info for k in ['userName', 'passWord']):
			return 'Cannot find username and password key'
		user, pswd = info['userName'], info['passWord']

## replace here with select user and pswd from database 
		if user == 'root' and pswd == '1234': 
			return redirect(url_for('pages.user_profile', uid=1))
		return render_template("login_page.html", logged="false")

	return render_template("login_page.html", logged="true")

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
    date = time.strftime('%Y-%m-%d')
    query = '''Insert into Accounts (
        account_name, open_date, uid) values (
        %s, %s, %d) ''' 
    ret = utils.setter_db(query, (name, date, uid))
    query = 'SELECT email FROM Users WHERE id=%d'
    email = utils.getter_db(query, (uid))[0][0]
    ret['user_email'] = email
    ret['account_id'] = ret.pop('last_insert_index')
    return jsonify(ret)
    	
@accounts.route('/<int:uid>/<int:accid>', methods=['GET', 'DELETE'])
def sub_account(uid, accid):
    ret = {"status":False}
    if request.method == 'GET':
	    query = '''SELECT U.email, A.account_name, A.open_date
		        FROM Users U JOIN Accounts A ON U.id=A.user_id
		        WHERE U.id=%d AND A.id=%d'''
	    ret = utils.getter_db(query, (uid, accid))
	    info = ret.pop('result')[0]
	    ret['user_email'] = info[0]
	    ret['account_name'] = info[1]
	    ret['open_date'] = info[2]
	    ret['user_id'] = uid
	    return jsonify(ret)
    elif request.method == 'DELETE':
        query = '''SELECT account_name FROM Accounts 
	             WHERE id=%d AND user_id=%d'''
        ret = utils.getter_db(query, (accid, uid))
        data = ret.pop('result')[0]
        ret['deleted_account_name'] = data[0]        
        date = time.strftime('%Y-%m-%d')
        ret['close_date'] = date
        query = 'UPDATE Accounts SET close_date=%s WHERE id=%d'
        utils.setter_db(query, (date, accid))
        return jsonify(ret)
	       
	    
	    
	
