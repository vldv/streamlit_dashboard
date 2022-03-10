# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 03:42:09 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import pandas as pd
import streamlit as st
from matplotlib import cm

import plotly.express as px
import plotly.graph_objects as go

from portfolio_utils import load_portfolio, tradedate_2_dtime, calc_gains
from viz_utils import sunbst_cmap
from finance_utils import get_yf_data


#%%

def main():
    
# load data and forex ticks

    pf = load_portfolio()
    pf['Trade Date'] = tradedate_2_dtime(pf['Trade Date'])
    currencies = set(pf['currency'])
    forex_ticks = ['EUR{}=X'.format(curr.upper()) for curr in currencies if curr != 'EUR']

        
#%% chart data load
    
    with st.form("screen_form"):
        
        interval_options = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
        interval = st.select_slider('Data interval:', options = interval_options, value = '1d')
        
        period_options = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
        period = st.select_slider('History range:', options = period_options, value = '6mo')
        
        st.form_submit_button("Submit")
        
        if interval_options.index(interval) < interval_options.index('1d') and period_options.index(period) > period_options.index('3mo'):
            st.warning('Cannot get intraday data for period larger than 1 month!')
            st.stop()
            
    hist = get_yf_data(list(set(pf['Symbol'])), interval, period).dropna()
    forex = get_yf_data(forex_ticks, interval, period).dropna()
    
    
#%% general statistics

    with st.expander("Repartition"):
        
        ticker_sumed = pf.groupby('Symbol', as_index=False).agg(
            {"Value":"sum",
             "sector":"first",
             "country":"first",
             "shortName":"first"})
    
        st.write('Country repartition, and sectors breakdown')
        col1, col2 = st.columns(2)
        with col1:
            col_data = ticker_sumed.groupby('country', as_index=False).agg({"Value":"sum"}).sort_values('Value')
            scol = sunbst_cmap(cm.Greens, col_data['country'], col_data['Value'])
            fig = px.sunburst(ticker_sumed,
                              path=['country', 'sector'],
                              values='Value',
                              color='country',
                              color_discrete_map = scol)
                           #   textinfo='label+percent parent')
            angle = 90 + 360 * (1 - col_data['Value'].iat[-1] / col_data['Value'].sum())
            fig.update_traces(rotation = angle, selector = dict(type='sunburst'), textinfo='label+percent root')
            fig.update_layout(margin_t=0, margin_r=0, margin_l=0, margin_b=0)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            col_data = ticker_sumed.groupby('sector', as_index=False).agg({"Value":"sum"}).sort_values('Value')
            scol = sunbst_cmap(cm.Oranges, col_data['sector'], col_data['Value'])
            fig = px.sunburst(ticker_sumed,
                              path=['sector', 'Symbol'],
                              values='Value',
                              color='sector',
                              color_discrete_map = scol)
            angle = 90 + 360 * (1 - col_data['Value'].iat[-1] / col_data['Value'].sum())
            fig.update_traces(rotation = angle, selector = dict(type='sunburst'), textinfo='label+percent root')
            fig.update_layout(margin_t=0, margin_r=0, margin_l=0, margin_b=0)
            st.plotly_chart(fig, use_container_width=True)
    
#%%
        
    with st.expander("Index benchmark"):
        col1, col2, col3 = st.columns(3)
        
        # total revenue vs CAC, SP, NASDAQ
        
#%%
        
    with st.expander("Revenue distribution"):
        
        revenues = calc_gains(pf, hist, forex)
        revenues = revenues.groupby("Symbol").sum().sort_values("Total").reset_index()
        n = len(revenues)
        
        fig = px.bar(revenues, x="Symbol", y=["Total"])
        fig.update_traces(marker_color=['darkgoldenrod']*n, selector={'name':'Total'})
        fig.update_layout(margin_b=0, margin_r=20)
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(revenues, x="Symbol", y=["Underlying", "Forex", "Dividends"])
        fig.update_traces(marker_color=['goldenrod']*n, selector={'name':'Underlying'})
        fig.update_traces(marker_color=['gold']*n, selector={'name':'Forex'})
        fig.update_traces(marker_color=['palegoldenrod']*n, selector={'name':'Dividends'})
        fig.update_layout(margin_t=0)
        st.plotly_chart(fig, use_container_width=True)
        
#%%

    with st.expander("Diversification"):
        col1, col2 = st.columns(2)
        with col1:
            pearson_matrix = hist.swaplevel(0, 1, axis=1).reset_index()['Close'].corr('pearson')
            fig = px.imshow(pearson_matrix, range_color=[-1, 1], color_continuous_scale='RdBu_r')
            fig.update_traces({'showscale':False, 
                               'coloraxis':None, 
                               'colorscale':'RdBu_r'},
                              selector={'type':'heatmap'})
            fig.update_layout(margin_t=0, margin_r=0, margin_l=0, margin_b=0)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            values = ticker_sumed['Value'].values
            value_coef = values[None,:] * values[:, None]
            for i in range(len(value_coef)):
                value_coef[i,i] = 0 #annule le poids d'autocorrelation
            divimp = pd.concat([pearson_matrix.mean(0),
                                    (value_coef * pearson_matrix).mean(0)],
                               axis=1)
            divimp.columns=(['Raw impact', 'Value normalized'])
            divimp = divimp.sort_values('Value normalized')
            divimp = divimp / divimp.abs().max(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(y=divimp.index,
                                 x=divimp['Raw impact'],
                                 name='Raw impact',
                             #    marker_color = sym_cmap(cm.RdBu_r, divimp['Raw impact']),
                                 orientation='h'))
            fig.add_trace(go.Bar(y=divimp.index,
                                 x=divimp['Value normalized'],
                                 name='Value impact',
                              #   marker_color = sym_cmap(cm.RdBu_r, divimp['Value normalized']),                     
                                 orientation='h'))
            fig.update_yaxes(autorange=True)
            fig.update_layout(margin_t=0, margin_r=0, margin_l=0, margin_b=0)
            st.plotly_chart(fig, use_container_width=True)
            
#%%
        
    with st.expander("Trend and dynamics"):
        col1, col2, col3 = st.columns(3)
        #faceted plot with 50, 200 RMA, etc
    