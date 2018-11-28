from flask import request, jsonify, Blueprint, current_app, session, render_template

import traders_back.utils as utils
import traders_back.manage as manage
import datetime


chart = Blueprint('chart', __name__)
virtual_time = datetime.datetime(2018,1,1,18,0,0)

@chart.route('/chart_api')
def chart_api():
	return "candle api"
	
	
@chart.route('/chart_point', methods=['GET', 'POST'])
def chart_points():
	req = utils.get_req_data()
	fr = req['currency_from']
	to = req['currency_to']
	q =\
	"""
	SELECT * FROM ExchangeRates 
	WHERE TIME>%s
	AND currency_from=%s and currency_to=%s
	LIMIT 1
	"""
	
	if not "virtual_time" in session:
		session['virtual_time'] = virtual_time

	ret = utils.getter_db(q, (session['virtual_time'], fr, to))['result'][0]
	session['virtual_time'] = ret['time']
	return jsonify(ret)

@chart.route('/chart_candle', methods=['POST'])
def chart_candle():
	return ""

@chart.route('/chart_clear')
def chart_clear():
	session.clear()
	return ""

@chart.route('/virtual_time')
def get_virtual_time():
	if not "virtual_time" in session:
		session['virtual_time'] = virtual_time
	return jsonify(session['virtual_time'])
	
