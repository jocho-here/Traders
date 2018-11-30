from flask import request, jsonify, Blueprint

import traders_back.utils as utils
import traders_back.manage as manage

positions = Blueprint('positions', __name__)


@positions.route('/users/<int:user_id>/accounts/<int:account_id>/positions', methods=['GET', 'POST'])
def position_management(user_id, account_id):
    rtn_val = {}
    req = utils.get_req_data()
    print(req)

    # TODO:Check if user_id and account_id are together
    if request.method == 'GET':
        rtn_val = manage.get_positions(account_id)
    elif request.method == 'POST':
        if 'currency_from' in req and 'currency_to' in req and \
           'time' in req and 'position_type' in req and 'volume' in req:
            rtn_val = manage.create_position(\
                          account_id, req['currency_from'].strip(), req['currency_to'].strip(), req['time'].strip(), \
                          req['position_type'], req['volume']\
                      )
        else:
            rtn_val['status'] = False
            rtn_val['message'] = "Request is missing either currency_from, currency_to, time, position_type, or volume"

    return jsonify(rtn_val)

@positions.route('/users/<int:user_id>/accounts/<int:account_id>/positions/from/<from_date>/to/<to_date>', methods=['GET'])
def positions_in_date(user_id, account_id, from_date, to_date):
    rtn_val = {}

    # TODO:Check if user_id and account_id are together
    if request.method == 'GET':
        rtn_val = manage.get_positions(account_id, from_date=from_date, to_date=to_date)

    return jsonify(rtn_val)

@positions.route('/users/<int:user_id>/accounts/<int:account_id>/positions/from/<from_date>/to/<to_date>/status/<status>', methods=['GET'])
def positions_in_date_and_status(user_id, account_id, from_date, to_date, status):
    rtn_val = {}

    # TODO:Check if user_id and account_id are together
    if request.method == 'GET':
        rtn_val = manage.get_positions(account_id, from_date=from_date, to_date=to_date, status=status)

    return jsonify(rtn_val)

@positions.route('/users/<int:user_id>/accounts/<int:account_id>/positions/status/<status>', methods=['GET'])
def positions_status(user_id, account_id, status):
    rtn_val = {}

    # TODO:Check if user_id and account_id are together
    if request.method == 'GET':
        rtn_val = manage.get_positions(account_id, status=status)

    return jsonify(rtn_val)

@positions.route('/users/<int:user_id>/accounts/<int:account_id>/positions/<int:position_id>', methods=['GET', 'PUT'])
def specific_position(user_id, account_id, position_id):
    rtn_val = {}
    req = utils.get_req_data()

    # TODO:Check if user_id and account_id are together
    # TODO:Check if account_id and position_id are together
    if request.method == 'GET':
        rtn_val = manage.get_position_from_id(position_id)
    elif request.method == 'PUT':
        if 'close_rate_time' in req and 'open_rate_id' in req:
            rtn_val = manage.close_position(position_id, req['close_rate_time'])
        else:
            rtn_val['status'] = False
            rtn_val['message'] = "Request is missing close_rate_time"

    return jsonify(rtn_val)
