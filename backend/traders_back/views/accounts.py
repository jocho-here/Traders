from flask import session, flash, jsonify, Blueprint, render_template, request, redirect, url_for
import traders_back.utils as utils
import traders_back.manage as manage

accounts = Blueprint('accounts', __name__)
import datetime

@accounts.route('/account_page', methods=['POST'])
def account_page():
    req = utils.get_req_data()
    print('----------------------')
    print('account_page')
    print('req: ', req)

    uid = req['uid']
    account_id = req['account_id']
    account_name = req['account_name']

    print('uid: ', uid)
    print('account_id: ', account_id)
    print('account_name: ', account_name)
    print('----------------------')

    return render_template('Account/index.html', uid=uid, account_id=account_id, account_name=account_name)

@accounts.route('/create_account', methods=['POST'])
def page_create_account():
    req = utils.get_req_data()

    return render_template('create_account.html', uid=req['uid'], user=req['user'])

@accounts.route('/account')
def account_apis():
    return "Accounts"

@accounts.route('/new_account', methods=['POST'])
def create_new_account():
    req = utils.get_req_data()

    uid = int(req['uid'])
    name = req['account_name']
    equity = req['equity']
    ret = manage.create_account(uid, name, equity) 

    if not ret['status']:
        flash("Account name already taken")
        return render_template('create_account.html', uid=uid, user=req['user'])

    query = 'SELECT email FROM Users WHERE id=%s'
    email = utils.getter_db(query, (uid))['result'][0]['email']
    ret['user_email'] = email

    session['accounts'] = manage.get_user_accounts(uid)['accounts']

    flash("Successfully created a new account")
    return redirect(url_for('users.user_page', uid=uid, user=req['user']))
    	
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
    
    
@accounts.route('/account_balance', methods=['POST'])
def get_account_balance():
	#get earnings of open positions based on current price before given time
	req = utils.get_req_data()
	accid = req['account_id']
	time = datetime.datetime.strptime(req['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
	q =\
	"""
	SELECT currency_from, currency_to, sum(volume*(latest-ask)) as earnings 
	FROM (
		SELECT E.ask as latest, T2.* from ExchangeRates E 
		NATURAL JOIN (
			SELECT max(id) as id 
			FROM (
				select E.id,  E.currency_from, E.currency_to from ExchangeRates E 
				join (
					select DISTINCT E.currency_from, currency_to 
					from Positions P 
					join ExchangeRates E 
					on P.open_rate_id = E.id 
					where P.position_status='open' 
					and P.account_id=%s
				) P 
				on E.currency_from=P.currency_from 
				and E.currency_to=P.currency_to 
				where time < %s 
			) T 
			GROUP BY currency_from, currency_to) T1 
			JOIN (
				select P.volume, E.ask, E.currency_from, E.currency_to 
				from Positions P 
				JOIN ExchangeRates E on E.id=P.open_rate_id 
				where P.position_status='open'
				and P.account_id=%s
			) T2 
			on E.currency_from=T2.currency_from 
			and E.currency_to = T2.currency_to
		) F 
		group by currency_from, currency_to;
	"""
	ret = utils.getter_db(q, (accid, time, accid))['result']
	q =\
	"""
	SELECT available_equity FROM Accounts where id=%s
	"""
	equity = utils.getter_db(q, (accid))['result'][0]['available_equity']
	for e in ret:
		equity += e['earnings']
		
	
	return jsonify({
		'accid': accid,
		'balance': equity
		})
