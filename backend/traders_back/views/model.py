from flask import request, jsonify, Blueprint
import json
import traders_back.utils as utils
import traders_back.manage as manage

model = Blueprint('model', __name__)

class Status:
	def __init__(self, f, t, s, e):
		self.status = { 
			'currency_from': f,
			'currency_to': t,
			'balance': 0,
			'total_cost': 0,
			'unrealized_balance': 0,
			'holdings': 0,
		}
		#<STATUS>: <POSITION TYPE> <AMOUNT> volume <CURR_FROM> to <CURR_TO> at <TIME> with rate $<RATE>
		#Example:
		# ACCEPTED/REJECTED: BUY 111.23 volume USD to JPY at 2018-01-14 19:37:50 with rate $100.0
		self.log = []
		self.retrieve_history(f, t, s, e)
		self.last_position = self.exchangeRates[-1]
	
	def get_positions(self):
		return self.exchangeRates
	
	def retrieve_history(self, f, t, s, e):
		q =\
		"""
		SELECT * FROM ExchangeRates 
		WHERE currency_from=%s AND currency_to=%s 
		AND (time >= %s and time <= %s)
		"""
		self.exchangeRates = utils.getter_db(q, (f, t, s, e))['result']
		
	
	# p: Limit price, v: volume
	def open_position(self, p, v, skip=1):
	#	for idx, position in enumerate(
	#			self.exchangeRates[self.last_position:], 
	#			self.last_position):
		accept = False
		for idx, position in enumerate(self.exchangeRates):
			if p >= position['ask']:
				p = position['ask']
				self.status['total_cost'] += p*v
				#self.status['unrealized_balance'] += p*v
				self.status['holdings'] += v
				#self.last_position = idx
				self.exchangeRates = self.exchangeRates[idx+skip:]
				accept = True
				self.write_log(True, 'BUY', p, v, time=position['time'])
				break
		if not accept:
			self.write_log(False, 'BUY', p, v)
		return accept
		
	def close_position(self, p, v, skip=1):
		accept = False
		#if self.status['holdings']
		for idx, position in enumerate(self.exchangeRates):
			if p <= position['bid']:
				p = position['bid']
				self.status['total_cost'] -= p*v
				self.status['holdings'] -= v
				self.exchangeRates = self.exchangeRates[idx+skip:]
				accept = True
				self.write_log(True, 'SELL', p, v, time=position['time'])
				break
		if not accept:
			self.write_log(False, 'SELL', p, v)
		return accept
		
	def write_log(self, accept, t, p, v, time=None):
		if accept:
			clog = 'ACCEPTED: %s %s volume %s to %s at %s with rate $%s'%(
				t, v, self.status['currency_from'], 
				self.status['currency_to'], time, p)
		else:
			clog = 'CANCELED: %s %s volume %s to %s with rate $%s'%(
				t, v, self.status['currency_from'], 
				self.status['currency_to'], p)
			
		self.log.append(clog)
		
	def get_status(self):
		if self.status['holdings'] > 0:
			self.status['unrealized_balance'] =  self.status['holdings'] * self.last_position['bid']
		else:
			self.status['unrealized_balance'] = -self.status['holdings'] * self.last_position['ask']
		self.status['balance'] = self.status['unrealized_balance'] - self.status['total_cost']
		self.status['balance'] = utils.format_float(self.status['balance'])
		self.status['total_cost'] = utils.format_float(self.status['total_cost'])
		self.status['unrealized_balance'] = utils.format_float(self.status['unrealized_balance'])
		self.status['logs'] = self.log
		return self.status
	
	
	
@model.route('/model')
def model_api():
	return "model_api"
	
"""
Given a list of buy and sell prices, execute each sequentially
"""
@model.route('/sequenced_model', methods=['POST'])
def sequenced_model():
	req = utils.get_req_data()
	#print(type(req), req)

	curr_from = req['curr_from']
	curr_to = req['curr_to']
	start = req['time_from']
	end = req['time_to']
	
	status = Status(curr_from, curr_to, start, end)
	#positions = status.exchangeRates
	
	for p in req['positions']:
		if p['type'] == 'long':
			status.open_position(p['price'], p['volume'])
		elif p['type'] == 'short':
			status.close_position(p['price'], p['volume'])
			
	return jsonify(status.get_status())

"""
Given two resistances, buy and sell given the price, check every 30 minutes. 
"""
@model.route('/resistance_model', methods=['POST'])
def resistance_model():
	req = utils.get_req_data()
	curr_from = req['curr_from']
	curr_to = req['curr_to']
	start = req['time_from']
	end = req['time_to']
	offset = req['offset']
	above = req['above'] + offset
	below = req['below'] + offset
	volume = req['volume']
	
	status = Status(curr_from, curr_to, start, end)
	while True:
		if not status.open_position(below, volume, skip=30) and not status.close_position(above, volume, skip=30):
			return jsonify(status.get_status())
		
	return ""

"""
Find the 80% range of price fallen within the given date
"""
@model.route('/find_resistance', methods=['POST'])
def find_resistance():
	req = utils.get_req_data()
	
	curr_from = req['curr_from']
	curr_to = req['curr_to']
	start = req['time_from']
	end = req['time_to']
	
	q =\
	"""
	select ask from ( 
		select ask, @counter :=@counter+1 count
		from (select @counter:=0) initval, ExchangeRates 
		where currency_from=%s and currency_to=%s and (
			time>=%s and time<=%s
		) order by ask
	) T 
	where count = floor(0.2*@counter) 
	or count = ceil(0.8*@counter)
	"""
	res = utils.getter_db(q, (curr_from, curr_to, start, end))['result']
	rtv_val = {
		'indicator': '80% percent of ask price fall between the first resistance',
		'first_resistance_below': res[0]['ask'],
		'first_resistance_above': res[1]['ask']
	}
	
	return jsonify(rtv_val)
	
	
