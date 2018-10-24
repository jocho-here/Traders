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
	
@accounts.route('/new_account', methods=['POST'])
def create_new_account():
	ret = {"status":False, 
		"message":"Successfully created a new sub-account", 		"user_email":None, "account_name":None, "account_id": None}
	uid = request.args.get('uid')
	if not uid:
		ret["message"] = "usage: </new_account?uid=INT>"
		return jsonify(ret)
	uid = int(uid)
	if "name" not in reqeust.form:
		ret["message"] = "Received data missing name"
		return 	jsonify(ret)
	name = request.form["name"]
	date = time.strftime('%Y-%m-%d')
	query = '''Insert into Accounts (
			account_name, open_date, uid) values (
			"%s", "%s", %d) ''' 
	err, accountid = setter_db_id(query, (name, date, uid))
	if err:
		ret["message"] = err
		return ret
	query = 'SELECT email FROM Users where id=%d'
	data = utils.dict_getter_db(query, (uid))[0]
	if len(data) == 0:
		ret["message"] = 'No user with such id'
		return jsonify(ret)
	ret["user_email"] = data['email']
	ret["account_id"] = accountid
	ret["status"] = True
	return jsonify(ret)	
	
	
@accounts.route('/<int:uid>/<int:accid>', methods=['GET', 'DELETE'])
def sub_account(uid, accid):
    ret = {"status":False}
    if request.method == 'GET':
	    query = '''SELECT U.email, A.account_name, A.open_date
		        FROM Users U JOIN Accounts A ON U.id=A.user_id
		        WHERE U.id=%d AND A.id=%d'''
	    data = utils.getter_db(query, (uid, accid))
	    if not data:
		    ret["message"] = 'Account id does cooparate with User id'
		    return jsonify(ret)
	    data = data[0]
	    ret['status'] = True
	    ret['user_id'] = uid
	    ret['user_email'] = data[0]
	    ret['account_name'] = data[1]
	    ret['open_date'] = data[2]
	    return jsonify(ret)
    elif request.method == 'DELETE':
        query = '''SELECT account_name FROM Accounts 
	             WHERE id=%d AND user_id=%d'''
        result = getter_db(query, (accid, uid))
        if not result:
            ret['message'] = 'Account id does cooparate with User id'
            return jsonify(ret)
        ret['deleted_account_name'] = result[0][0]   
        ret['status'] = True
        date = time.strftime('%Y-%m-%d')
        ret['close_date'] = date
        ret['message'] = 'Successfully delete the account'
        query = '''UPDATE Accounts SET close_date=%s
                WHERE id=%d AND user_id=%d'''
        setter_db(query, (accid, uid))
        return jsonify(ret)
	       
	    
	    
	
