from flask import request, jsonify, Blueprint

import traders_back.utils as utils
import traders_back.manage as manage

exchange_rates = Blueprint('exchange_rates', __name__)


@exchange_rates.route('/exchangerates/currency_from/<currency_from>/currency_to/<currency_to>/from_time/<from_time>/to_time/<to_time>', methods=['GET'])
def getting_exchange_rates(currency_from, currency_to, from_time, to_time):
    rtn_val = {}
    req = utils.get_req_data()
    
    if request.method == 'GET':
        from_time = from_time.replace('_', ' ')
        to_time = to_time.replace('_', ' ')
        rtn_val = manage.get_exchange_rates(currency_from, currency_to, from_time=from_time, to_time=to_time)
        
    return jsonify(rtn_val)
