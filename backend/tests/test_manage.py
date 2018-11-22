# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
import time
sys.path.extend(['', '/home/bryce/classes/CS411/Traders/backend/tests', '/home/bryce/classes/CS411/Traders/backend/dist/traders_back-0.0.1-py3.6.egg', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python36.zip', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6/lib-dynload', '/home/bryce/miniconda3/envs/411/lib/python3.6', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6/site-packages', '/home/bryce/classes/CS411/Traders/backend'])

from traders_back import manage, utils

def test_users():
    for i in range(10):
        test_email = "test_email@email.com" + str(i)
        test_name = "testuname" + str(i)
        test_pass = "testpass" + str(i)
        delete_response = manage.delete_user(test_email, test_pass)
        
    test_email = "test_email@email.com0"
    test_name = "testuname0"
    test_pass = "testpass0"
    old_users = manage.get_all_users()['users']
    signup_response = manage.sign_up(test_email, test_name, test_pass)
    uid = signup_response['user_id']
    
    error = None
    try:
        for i in range(10):
            test_email = "test_email@email.com" + str(i)
            test_name = "testuname" + str(i)
            test_pass = "testpass" + str(i)
            signup_response = manage.sign_up(test_email, test_name, test_pass)
            if i == 0:
                assert not signup_response['status'] 
            else:
                assert signup_response['status']
        
            new_users = manage.get_all_users()['users']
        assert len(old_users) == len(new_users) - 10
    except Exception as e: 
        error = e
        raise #Change to raise if you want to see where the error occured 
    
    for i in range(10):
        test_email = "test_email@email.com" + str(i)
        test_name = "testuname" + str(i)
        test_pass = "testpass" + str(i)
        delete_response = manage.delete_user(test_email, test_pass)
#    
    if error is not None:
        raise error
        
def test_accounts():
    try:
        test_email = "test_email@email.com0"
        test_name = "testuname0"
        test_pass = "testpass0"
        signup_response = manage.sign_up(test_email, test_name, test_pass)
        uid = signup_response['user_id']
        #user_initial_accounts = manage.get_user_accounts(uid)
        #assert len(user_initial_accounts['accounts']) == 0 #MAY CHANGE if we want users to initally have an account
        
        test0_id = manage.create_account(uid, "test_acc0")['account_id']
        user_accounts = manage.get_user_accounts(uid)
        assert len(user_accounts['accounts']) == 1
        
        dup_account_status = manage.create_account(uid, "test_acc0")['status']
        assert not dup_account_status
        
        test1_id = manage.create_account(uid, "test_acc1")['account_id']
        user_accounts = manage.get_user_accounts(uid)
        assert len(user_accounts['accounts']) == 2
        
        delete_results = manage.delete_account(uid, test1_id)
        missing_acc_info = manage.get_account_info(test1_id)
        assert not missing_acc_info['status']
        
        user_accounts = manage.get_user_accounts(uid)
        acc1_info = manage.get_account_info(test0_id)
        assert acc1_info['account_info'] == user_accounts["accounts"][0]
        
        delete_response = manage.delete_user(test_email, test_pass)
    except:
        delete_response = manage.delete_user(test_email, test_pass)
        raise
     
def test_exchange_rates():
    try:
        nowish = (datetime.now() - timedelta(days=10)).replace(microsecond=0)
        starttime = nowish - timedelta(days=1)
        endtime = nowish + timedelta(days=1)
        topair = "GBP"
        frompair = "USD"
#        get_exch_status = manage.get_exchange_rates(frompair, topair, from_time=starttime, to_time=endtime)
#        print(get_exch_status)
#        old_exch_rates = get_exch_status['exchange_rates']
        now = nowish
        for i in range(10):
            for frompair in ["USD", "AUD", "CAD"]:
                for topair in ["GBP", "EUR", "JPY"]:
                    now = (now + timedelta(seconds=2)).replace(microsecond=0)
                    assert now > starttime
                    assert now < endtime
                    bid = 0.8 +i
                    ask = 0.7 + i
                    manage.add_exchange_rate(frompair, topair, bid, ask, now)
                    get_exch_status = manage.get_exchange_rates(frompair, topair, time=now)
                    get_exch_status['exchange_rate'].pop('id', None)
                    assert get_exch_status['currency_from'] == frompair
                    assert get_exch_status['currency_to'] == topair
                    assert get_exch_status['exchange_rate'] 

        get_exch_status = manage.get_exchange_rates(frompair, topair, from_time=starttime, to_time=endtime)
#        print(len(get_exch_status['exchange_rates']))
#        print(len(old_exch_rates))
#        assert len(get_exch_status['exchange_rates']) - len(old_exch_rates) == 10
    except:
        raise
        
    
def test_positions():
    try:
        test_email = "test_email@email.com0"
        test_name = "testuname0"
        test_pass = "testpass0"
        signup_response = manage.sign_up(test_email, test_name, test_pass)
        uid = signup_response['user_id']
        test0_id = manage.create_account(uid, "test_acc0")['account_id']
        user_accounts = manage.get_user_accounts(uid)
        get_positions_response = manage.get_positions(test0_id)
#        assert len(get_positions_response['positions']) == 0
        
        for i in range(10):
            now = datetime(2018, 1, 15+i)
            acc_info = manage.get_account_info(test0_id)
            create_pos_status = manage.create_position(test0_id, "USD", "GBP", now, position_type='long', volume=10000)
            pos_id = create_pos_status['position_id']
            get_positions_response = manage.get_positions(test0_id)
            assert len(get_positions_response['positions']) == i+1
            
            now += timedelta(minutes=30)
            manage.close_position(pos_id, now)
            get_positions_response = manage.get_positions(test0_id)
            position = get_positions_response['positions'][0]
            print(position)
            assert position['position_status'] == 'closed'
#        delete_response = manage.delete_user(test_email, test_pass)
    except:
        delete_response = manage.delete_user(test_email, test_pass)
        raise
    
#test_users()
#test_accounts()
#test_exchange_rates()
test_positions()
    
