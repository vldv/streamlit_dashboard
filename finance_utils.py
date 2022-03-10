# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 00:29:56 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import pandas as pd
import streamlit as st
import yfinance as yf


@st.cache(ttl=600, max_entries=10) # 10min, 10 entries
def get_yf_data(tick_list, interval, period):
    """ todo """
    if len(tick_list) > 1:
        yf_api = yf.Tickers(tick_list)
        df_full = yf_api.history(interval = interval, period = period).swaplevel(0, 1, axis=1).reset_index()
    elif len(tick_list) == 1:
        yf_api = yf.Ticker(tick_list[0])
        df_full = yf_api.history(interval = interval, period = period).reset_index()
        df_full.columns = pd.MultiIndex.from_tuples([('AAPL', c) for c in df_full.columns])
    else:
        st.warning('Please input at least one ticker.')
        st.stop()
    
    return df_full

    
def normalize(df, tick_list, mode):
    """ todo """
    index = {'First': 0, 'Last': len(df)-1}[mode]
    for tick in tick_list:
        for value in ['Open', 'Low', 'High', 'Close']:    
            df.loc[:, (tick, value)] = df.loc[:, (tick, value)]/df.loc[index, (tick, value)]
    return df