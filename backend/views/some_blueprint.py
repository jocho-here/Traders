from flask import jsonify, Blueprint, render_template, request, redirect, url_for


# This is where we create API endpoints for interacting with frontend

pages = Blueprint('pages', __name__)

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

@pages.route('/profile')
def user_profile():
	uid = request.args.get('uid')
	if not uid:
		return "usage: </profile?uid=INT>"
	return 'user_id: ' + str(uid)
	
