# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 08:25:20 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import numpy as np
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from finance_utils import get_yf_data, normalize


def main():
    #%% inputs 
    
    col1, col2 = st.columns([1,3])
    
    with col1:
        with st.form("screen_form"):
        
            tick_list = st.text_input('Space-sperated ticker list:', 'NVDA INTC AMD').split()
            tick_list = [tick.replace(',', '').upper() for tick in tick_list]
            
            interval_options = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
            interval = st.select_slider('Data interval:', options = interval_options, value = '1d')
            
            period_options = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
            period = st.select_slider('History range:', options = period_options, value = '6mo')
            
            st.write('Cannot get intraday data for period larger than 1 month.')
            
            norm_point = st.selectbox('What should be the reference point for normalization?',
             ('None', 'First', 'Last'), index = 0)
            
            st.form_submit_button("Submit")
            
            if interval_options.index(interval) < interval_options.index('1d') and period_options.index(period) > period_options.index('3mo'):
                st.warning('Cannot get intraday data for period larger than 1 month!')
                st.stop()
                
        #%% yfinance api call
        
        #try:
        df_full_immutable = get_yf_data(tick_list, interval, period)
        df_full = df_full_immutable.copy()
        
        if norm_point != 'None':
            df_full = normalize(df_full, tick_list, norm_point) 
        #except:
        #    st.warning('Something went wrong with the Yahoo Finance API call, check streamlit logs for more informations.')
        #    st.stop()
    
    
    #%% dataframe visualisation
    
    with col2:
        color_list = ['cyan', 'blue', 'magenta']
        fig = go.Figure()
        for tick, color in zip(tick_list, color_list):
            
            fig.add_trace(go.Candlestick(x=df_full['Date'],
                        open=df_full[tick]['Open'], high=df_full[tick]['High'],
                        low=df_full[tick]['Low'], close=df_full[tick]['Close'],
                        increasing_line_color= color, decreasing_line_color= 'gray'
                        ))
        
        st.plotly_chart(fig, use_container_width=True)

    return None

    