import requests, json

headers = {"Content-Type": "application/json"}
p01 = {
	'price': 110.7,
	'volume': 100,
	'type': 'short'
}
p1 = {
	'price': 110.887,
	'volume': 100, 
	'type': 'long'
}
p2 = {
	'price': 110.600,
	'volume': 49, 
	'type': 'long'
}
p3 = {
	'price': 110.860,
	'volume': 149, 
	'type': 'long'
}
data = {
	'curr_from': 'USD',
	'curr_to': 'JPY',
	'time_from': '2018-01-14 00:00:00',
	'time_to': '2018-01-15 23:59:59',
	'positions': []
}

def sequenced_trading(data):
	data['positions'] += [p1, p2, p3]
	req = requests.post('http://localhost:8080/sequenced_model', json=data, headers=headers)
	data['positions'] = []
	print(req.text)

def resistance_model(data):
	req = requests.post('http://localhost:8080/find_resistance', json=data, headers=headers)
	print(req.text)
	return json.loads(req.text)
	
def test_result_using_resistance():
	data = {
		'curr_from': 'USD',
		'curr_to': 'JPY',
		'time_from': '2018-01-14 00:00:00',
		'time_to': '2018-01-15 23:59:59',
		'positions': []
	}
	resistance = resistance_model(data)
	above = resistance['first_resistance_above']
	below = resistance['first_resistance_below']
	### a day after 
	test = { 
		'curr_from': 'USD',
		'curr_to': 'JPY',
		'time_from': '2018-01-15 00:00:00',
		'time_to': '2018-01-15 23:59:59',
		'above': above,
		'below': below,
		'volume': 100,
		'offset': 0 #Offset value based on daily news
		#'positions': []
	}
	req = requests.post('http://localhost:8080/resistance_model', json=test, headers=headers)
	print("\nTrading with given resistance value in one day\n")
	print(req.text)

test_result_using_resistance()


