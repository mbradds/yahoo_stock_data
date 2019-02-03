#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 17:49:10 2019

@author: grant
"""

import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as web

def yahoo_data(url):

    index_url = str(url)
    index = pd.read_html(index_url,header = [0])[0]

    index_dict = {}
    pop_list = []
    for s,n in zip(index['Symbol'], index['Name']):
        #s = s.replace('^','')
        index_dict[s] = n



    for key in index_dict:
        index_dict[key] = pd.DataFrame()

        start = datetime.datetime(2000, 1, 1)
        end = datetime.datetime.now()
        try:
            index_dict[key] = web.DataReader(key, 'yahoo', start, end)
            idx = pd.date_range(start, end)
            index_dict[key] = index_dict[key].reindex(idx, fill_value=np.nan)
            df_index_1 = key.replace('^','')
            columns = pd.MultiIndex.from_arrays([[df_index_1]*6,
                                     ['High','Low','Open','Close','Volume','Adj Close']])
            index_dict[key].columns = columns
        except:
            print('couldnt get data for symbol:'+key)
            pop_list.append(key)
    
    for x in pop_list:
        index_dict.pop(x)
        
    #join all the dataframes together
    master_frame = pd.DataFrame()

    for key in index_dict:
        if master_frame.empty:
            master_frame = index_dict[key]
        else:
            master_frame = pd.merge(master_frame, index_dict[key], left_index=True, right_index=True, how='outer')
        
    return(master_frame)
    
url = 'https://sg.finance.yahoo.com/world-indices'
master = yahoo_data(url)
print(master.head())