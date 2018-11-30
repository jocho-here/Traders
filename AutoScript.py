#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import AutoModule
import random
from datetime import datetime, timedelta

def __main__():
    parser = argparse.ArgumentParser("Script to add downloaded exch rates")
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    args, _ = parser.parse_known_args()
    
    conn = AutoModule.Connection("http://localhost:8080", args.username, args.password)
    s = datetime.now() - timedelta(days=356)
    e = datetime.now()
    
    accounts = []
    accounts.append((conn.create_account("Discrete_acc{}".format(random.randint(0,100000))), AutoModule.DiscretePos))
    accounts.append((conn.create_account("Patient_acc{}".format(random.randint(0,100000))), AutoModule.PatientPos))
    rates = conn.get_rates("USD", "GBP", s, e)
    for index, rate in enumerate(rates):
        for acc, PObj in accounts:
            if len(acc.open_positions) == 0:
                p = acc.new_position(PObj, "USD", "GBP", 1000, datetime.now(), position_status=AutoModule.POS_WAITING)
            acc.show(rate)
        if index > 1000:
            break

if __name__ == "__main__":
    __main__()
