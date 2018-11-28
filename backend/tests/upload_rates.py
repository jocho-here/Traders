#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 19:21:49 2018

@author: bryce
"""

import argparse
import glob
import os

#REMOVE AT SUBMISSION
import sys
sys.path.extend(['', '/home/bryce/classes/CS411/Traders/backend/tests', '/home/bryce/classes/CS411/Traders/backend/dist/traders_back-0.0.1-py3.6.egg', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python36.zip', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6/lib-dynload', '/home/bryce/miniconda3/envs/411/lib/python3.6', '/home/bryce/.local/share/virtualenvs/backend-UR8qZ0SU/lib/python3.6/site-packages', '/home/bryce/classes/CS411/Traders/backend'])
##############

from traders_back import manage
import pandas as pd
from datetime import datetime, timedelta
from multiprocessing import Pool


DESIRED_PAIRS = ["AUD", "CAD", "CHF", "CNH", "EUR", "GBP", "JPY", "MXN", "NOK", "NZD", "SEK", "TRY", "USD", "ZAR"]
GRANULARITY = 100 # upload every 100th datapoint.

def upload_file(filename):
    exch1, exch2 = os.path.basename(filename)[2:].split('_')[:2]
    if exch1 not in DESIRED_PAIRS or exch2 not in DESIRED_PAIRS:
        return
    print("Uploading {}...".format(filename))
    rate_df = pd.read_csv(filename, compression="zip")
    latest_dt = datetime.min
    skip = 0
    for index, row in rate_df.iterrows():
        skip += 1
        if skip < GRANULARITY:
            continue
        else:
            skip = 0
        rate_dt = row["RateDateTime"] #str
        if '.' in rate_dt:
            p_index = rate_dt.index('.')
        else:
            p_index = len(rate_dt)
            rate_dt += ".000"
        stripped_dt = rate_dt[:p_index + 3]
        rate_dt = datetime.strptime(stripped_dt, "%Y-%m-%d %H:%M:%S.%f") # Datetime obj
        if rate_dt < latest_dt + timedelta(seconds=1):
            continue
        latest_dt = rate_dt
        currency_from, currency_to = row["CurrencyPair"].split('/')
        add_status = manage.add_exchange_rate(currency_from=currency_from,
                                 currency_to=currency_to,
                                 bid=row["RateBid"],
                                 ask=row["RateAsk"],
                                 time=rate_dt)
        addinv_status = manage.add_exchange_rate(currency_from=currency_to,
                                 currency_to=currency_from,
                                 bid=1/row["RateBid"],
                                 ask=1/row["RateAsk"],
                                 time=rate_dt)
            
def __main__():
    parser = argparse.ArgumentParser("Script to add downloaded exch rates")
    parser.add_argument("download_dir", type=str, help="Location of all .zip files from rategaincapital")
    parser.add_argument("-j", type=int, default=1, help="Number of uploader workers to use. Defaults to 1")
    args, _ = parser.parse_known_args()
    
    if args.j > 1:
        pool = Pool(processes=args.j)
        pool.map(upload_file, glob.iglob('{}/**/.*.zip'.format(args.download_dir), recursive=True))
    else:
        for filename in glob.iglob('{}/**/.*.zip'.format(args.download_dir), recursive=True):
            upload_file(filename)
            
if __name__=="__main__":
    __main__()