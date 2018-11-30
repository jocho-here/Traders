#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:29:23 2018

@author: bryce
"""

import requests 
from datetime import timedelta, datetime
from threading import Thread
from queue import Queue
import random

CHUNK_INTERVAL = timedelta(days=31)
QUEUE_MAXSIZE  = 50000
QUEUE_CAP = "QUEUE_CAP"
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
JSONIFY_DT_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

POS_WAITING = "WAITING"
POS_OPEN = "OPEN"
POS_CLOSED = "CLOSED"


def datetime_to_str(dt):
    if type(dt) is not str:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
def str_to_datetime(string, from_json=False):
    if type(string) is str:
        if from_json:
            return datetime.strptime(string, JSONIFY_DT_FORMAT)
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

class Account(object):
    
    def __init__(self, account_name, available_equity, connection=None, create=True, positions=[], account_id=None):
        self.account_name = account_name
        self.available_equity = available_equity
        self.positions = positions
        self.waiting_positions = []
        self.open_positions = []
        self.closed_positions = []
        self.connection = connection
        self.account_id = account_id
        if create:
            self.create_account()
        
    def create_account(self):
        url = "{}/script_new_account".format(self.connection.hostname)
        data = {"uid": self.connection.uid, "account_name": self.account_name, "equity": self.available_equity}
        print(data)
        req = requests.post(url=url, data=data)
        data = req.json()
        if not data["status"]:
            print(data["message"])
            return
        self.account_id = data["account_id"]
      
    def get_account_info(self):
        url = "{}/{}/{}".format(self.connection.hostname, self.connection.uid, self.account_id)
        req = requests.get(url)
        data = req.json()
        print(data)
        return data

    def new_position(self, PClass, currency_from, currency_to, volume, init_time, position_status=POS_WAITING):
        p = PClass(self, currency_from, currency_to, volume, init_time, position_status)
        self.waiting_positions.append(p)
        return p
        
    def show(self, rate):
        for p in self.waiting_positions + self.open_positions:
            if rate.currency_from == p.currency_from and rate.currency_to == p.currency_to:
                 if p.position_status is POS_WAITING or (p.position_status is POS_OPEN and rate.time > p.open_rate.time):
                     p.show_rate(rate)
        
class Position(object):
    
    def __init__(self, account, currency_from, currency_to, volume, init_time, position_status=POS_WAITING):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.init_time = init_time
        self.position_type = "open" #only type for now
        self.position_status = position_status
        self.volume = volume
        self.account = account
        
    def show_rate(self, rate):
        pass # This is where the position rule is implemented
        
    def open_pos(self, rate):
        url = "{}/users/{}/accounts/{}/positions".format(self.account.connection.hostname,
                                                           self.account.connection.uid,
                                                           self.account.account_id)
        data = {"currency_from": self.currency_from, 
                "currency_to": self.currency_to, 
                "volume": self.volume,
                "time": rate.time,
                "position_type": self.position_type}
        
        req = requests.post(url=url, data=data)
        data = req.json()
        if not data['status']:
            print(data['message'])
            return
        self.position_status = POS_OPEN
        self.open_rate = rate
        self.position_id = data['position_id']
        self.account.waiting_positions.remove(self)
        self.account.open_positions.append(self)
        print("Account {} is opening position @ {}".format(self.account.account_name, rate))
    
    def close_pos(self, rate):
        url = "{}/users/{}/accounts/{}/positions/{}".format(self.account.connection.hostname,
                                                           self.account.connection.uid,
                                                           self.account.account_id,
                                                           self.position_id)
        data = {"close_rate_time": rate.time} 
        req = requests.put(url=url, data=data)
#        data = req.json()
#        if not data['status']:
#            print(data['message'])
        self.position_status = POS_CLOSED
        self.close_rate = rate
        self.account.open_positions.remove(self)
        self.account.closed_positions.append(self)
        print("Account {} is closing position @ {}".format(self.account.account_name, rate))
        acc_info = self.account.get_account_info()
        print("Account {} value is now {}".format(self.account.account_name, acc_info["available_equity"])) 
        return
        
        
    
class Rate(object):
    
    def __init__(self, currency_from, currency_to, bid, ask, time):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.bid = bid
        self.ask = ask
        if type(time) is str:
            time = str_to_datetime(time)
        self.time = time
    
    def __str__(self):
        return "{}/{}@{}:\t{}b\t{}a".format(self.currency_from, self.currency_to, datetime_to_str(self.time), self.bid, self.ask)

def rate_supplier(rate_queue, hostname, currency_from, currency_to, start_time, end_time, chunk_interval):
    try:
        curr_time = start_time
        while curr_time <= end_time:
            url = "{}/exchangerates/currency_from/{}/currency_to/{}/from_time/{}/to_time/{}".format(hostname,
                                                                                                    currency_from,
                                                                                                    currency_to, 
                                                                                                    datetime_to_str(curr_time),
                                                                                                    datetime_to_str(min(curr_time+chunk_interval, end_time)))
            req = requests.get(url=url)
            data = req.json()
            if data["status"]: #If timedelta is too small, no rates will fall in that interval and thus the API call will return nothing
                for rate in data["exchange_rates"]:
                    dt_obj = str_to_datetime(rate["time"], from_json=True)
                    rate_queue.put(Rate(currency_from, currency_to, rate["bid"], rate["ask"], dt_obj))
            curr_time += chunk_interval
    except:
        print("rate_supplier caught error... closing queue")
        rate_queue.put(QUEUE_CAP)
        raise
    rate_queue.put(QUEUE_CAP)
    return

      
class Connection(object):
    
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.uid = None
        self.__login__(username, password)
        self.accounts_by_id = {}
        self.accounts_by_name = {}
    
    def __login__(self, username, password):
        signin_url = "{}/script_login".format(self.hostname)
        req = requests.post(signin_url, data={"userName": username, "passWord": password})
        data = req.json()
        if not data["status"]:
            print("Login unsucessful. Connection may still be used to retrieve rates")
            return False
        else:
            self.uid = data["uid"]
        
    
    def create_account(self, account_name, available_equity=100000):
        acc = Account(account_name, available_equity, connection=self)
        self.accounts_by_name[account_name] = acc
        self.accounts_by_id[acc.account_id] = acc
        return acc
        
    def get_rates(self, currency_from, currency_to, start_time, end_time):
        rate_queue = Queue(maxsize=QUEUE_MAXSIZE)
        rate_supplier_thread = Thread(target=rate_supplier, daemon=True, args=(rate_queue, 
                                                                              self.hostname, 
                                                                              currency_from, 
                                                                              currency_to, 
                                                                              start_time, 
                                                                              end_time, 
                                                                              CHUNK_INTERVAL,))
        rate_supplier_thread.start()
        curr_rate = rate_queue.get()
        while curr_rate != QUEUE_CAP:
            curr_rate = rate_queue.get()
            yield curr_rate
        rate_supplier_thread.join()
        return
    
  
class DiscretePos(Position):
    def __init__(self, account, currency_from, currency_to, volume, init_time, position_status=POS_WAITING ):
        super().__init__(account, currency_from, currency_to, volume, init_time, position_status)
        self.position_type = "Discrete"
        
    def show_rate(self, rate):
        if self.position_status is POS_WAITING:
            self.open_pos(rate)
        elif self.position_status is POS_OPEN:
            if rate.time - timedelta(hours=2) > self.open_rate.time:
                self.close_pos(rate)
        return    
    
    
class PatientPos(Position):
    def __init__(self, account, currency_from, currency_to, volume, init_time, position_status=POS_WAITING ):
        super().__init__(account, currency_from, currency_to, volume, init_time, position_status)
        self.position_type = "Patient"
        
    def show_rate(self, rate):
        if self.position_status is POS_WAITING:
            self.open_pos(rate)
        elif self.position_status is POS_OPEN:
            if rate.time - timedelta(hours=480) > self.open_rate.time or \
                    rate.ask/rate.bid > 1.000001:
                self.close_pos(rate)
        return    
