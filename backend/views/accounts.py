from flask import jsonify, Blueprint, render_template, request, redirect, url_for
import MySQLdb, os, time

# This is where we create API endpoints for interacting with frontend

pages = Blueprint('pages', __name__)
accounts = Blueprint('accounts', __name__)

USER = os.environ.get('cs411traders_user')
PSWD = os.environ.get('cs411traders_pswd')
db = MySQLdb.connect("localhost", USER, PSWD, "cs411traders_Traders")
cursor = db.cursor()


def execute_insert(q):
	try:
		cursor.execute(q)
		db.commit()
		return None
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		db.rollback()
		return err

@pages.route('/')
def start():

    return "cs411 traders"

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

"""
@pages.route('/account')
def user_account():
	accID = request.args.get('accID')
	if not accID:
		return "usage: </account?accID=INT"
	return render_template("user_account.html")
"""	
	
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
			"%s", "%s", %d) ''' %(name, date, uid)
	err = execute_insert(query)
	if err:
		ret["message"] = err
		return ret
	accountid = cursor.lastrowid
	query = 'SELECT email FROM Users where id=%d' %uid
	cursor.execute(query)
	data = cursor.fetchone()
	if len(data) == 0:
		ret["message"] = 'No user with such id'
		return jsonify(ret)
	ret["user_email"] = data[0]
	ret["account_id"] = accountid
	ret["status"] = True
	return jsonify(ret)	
	
@accounts.route('/account', methods=['GET', 'DELETE'])
def get_account_info():
	ret = {"status":False, 
			"message":"Successfully deleted a user",
			"deleted_user_email":None}
	accid = request.args.get("accId")
	if not accid:
		ret["message"] = "Usage: </account?accId=INT>"
		return jsonify(ret)
	accid = int (accid)
	if request.method == 'GET':
		return None
	elif request.method == 'DELETE':
		
		deleted = cursor.execute('DELETE FROM Accounts WHERE ID=%d' &accid)
		if deleted == 0:
			ret["message"] = "Account Id does not exist"
			return jsonify(ret)
		return None
		
	
	
