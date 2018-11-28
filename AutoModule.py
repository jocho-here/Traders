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


CHUNK_INTERVAL = timedelta(days=31)
QUEUE_MAXSIZE  = 50000
QUEUE_CAP = "QUEUE_CAP"
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
JSONIFY_DT_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


def datetime_to_str(dt):
    if type(dt) is not str:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
def str_to_datetime(string, from_json=False):
    if type(string) is str:
        if from_json:
            return datetime.strptime(string, JSONIFY_DT_FORMAT)
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

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
    
    def __login__(self, username, password):
        signin_url = "{}/verify_login".format(self.hostname)
        req = requests.post(signin_url, data={"userName": username, "passWord": password})
        data = req.json()
        if not data["status"]:
            print("Login unsucessful. Connection may still be used to retrieve rates")
            return False
        else:
            self.uid = data["uid"]
            
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
    
      
def test():
    conn = Connection("http://localhost:8080", "bkille", "abcd")
    s = datetime.now() - timedelta(days=356)
    e = datetime.now()
    
    rates = conn.get_rates("USD", "GBP", s, e)
#    for index, rate in enumerate(rates):
#        print(index, ':', rate)
test()
        