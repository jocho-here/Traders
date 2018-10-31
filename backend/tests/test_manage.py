# -*- coding: utf-8 -*-

import sys
sys.path.extend(['', '/home/bryce/classes/CS411/Traders/backend/tests', '/home/bryce/classes/CS411/Traders/backend/dist/traders_back-0.0.1-py3.6.egg', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python36.zip', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6/lib-dynload', '/home/bryce/miniconda3/envs/411/lib/python3.6', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6/site-packages', '/home/bryce/classes/CS411/Traders/backend'])

from traders_back import manage

def test_users():
    test_email = "test_email@email.com"
    test_name = "testuname"
    test_pass = "testpass"
    old_users = manage.get_all_users()['users']
    signup_response = manage.sign_up(test_email, test_name, test_pass)
    uid = signup_response['user_id']
    new_users = manage.get_all_users()['users']
    try:
        assert len(old_users) == len(new_users) - 1
    except AssertionError:
        delete_response = manage.delete_user(test_email, test_pass)
        raise
    delete_response = manage.delete_user(test_email, test_pass)
    
    for i in range(10):
        test_email = "test_email@email.com" + str(i)
        test_name = "testuname" + str(i)
        test_pass = "testpass" + str(i)
        signup_response = manage.sign_up(test_email, test_name, test_pass)
        
        
test_users()
    