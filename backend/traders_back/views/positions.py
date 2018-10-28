from flask import request, jsonify, Blueprint

import traders_back.utils as utils
import traders_back.manage as manage

positions = Blueprint('positions', __name__)


@positions.route('/users/<int:user_id>/accounts/<int:account_id>/positions', methods=['GET', 'POST'])
def position_management(user_id, account_id):
    rtn_val = {}
    req = utils.get_req_data()

    # TODO:Check if user_id and account_id are together
    if request.method == 'GET':
        rtn_val = manage.get_positions(account_id)
    elif request.method == 'POST':
        if 'currency_from' in req and 'currency_to' in req and \
           'time' in req and 'position_type' in req and 'volume' in req:

            rtn_val = manage.create_position(\
                          account_id, req['currency_from'], req['currency_to'], req['time'], \
                          req['position_type'], req['volume']\
                      )

    return jsonify(rtn_val)
