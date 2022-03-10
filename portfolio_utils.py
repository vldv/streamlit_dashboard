# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:31:33 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def make_portfolio(path_in = 'finance/quotes.csv', path_out = 'finance/portfolio.csv'):
    """ """
    # load
    pf = pd.read_csv(path_in)
    pf['Quantity'] = [0 if np.isnan(q) else q for q in pf['Quantity']]
    # remove "watch only"
    pf = pf.drop( pf.index[pf['Quantity'] < 1] )
    # portfolio = portfolio.sort_values(by=['Trade Date']).reset_index()
    
    # ajout de colonnes
    pf['Value'] = pf['Current Price'] * pf['Quantity']
    pf['Purchase Value'] = pf['Purchase Price'] * pf['Quantity']
    
    rel_info = ['currency',
                'sector',
                'country',
                'recommendationKey',
                'targetLowPrice',
                'targetMedianPrice',
                'targetHighPrice',
                'shortName',
                'shortRatio',
                'beta',
                'dividendYield'
                ]

    for info_item in rel_info:
        pf[info_item] = [''] * len(pf)
    
    for ticker in pf['Symbol']:
        print(ticker)
        infos = yf.Ticker(ticker).get_info()
        for info_item in rel_info:
            try:
                pf.loc[pf['Symbol'] == ticker, info_item] = infos[info_item]
            except KeyError:
                pf.loc[pf['Symbol'] == ticker, info_item] = None
                
    # corrections manuelles
    try:
        pf.loc[pf['Symbol']=="UST.PA", "sector"] = "ETF"
        pf.loc[pf['Symbol']=="UST.PA", "country"] = "USA"
        pf.loc[pf['Symbol']=="UST.PA", "country"] = "USA"
    except:
        pass
    
    try:
        pf.loc[pf['Symbol']=="UST.PA", "sector"] = "ETF"
        pf.loc[pf['Symbol']=="UST.PA", "country"] = "USA"
        pf.loc[pf['Symbol']=="UST.PA", "country"] = "USA"
    except:
        pass

    pf.to_csv(path_out)
    
    return pf


def load_portfolio(path = 'finance/portfolio.csv', make=False):
    """ """
    if make:
        make_portfolio(path_out = path)
    return pd.read_csv(path)


def calc_gains(pf, hist, forex):
    """ """
    gains_data = []
    iterable = zip( pf['Symbol'], pf['Quantity'], pf['Trade Date'], pf['currency'] )
    for tick, qty, td, cur in iterable:
        gains_data += [calc_gains_equity(tick, qty, td, cur, pf, hist, forex)]
        
    gains_df = pd.DataFrame(data=gains_data, columns=['Underlying', 'Forex', 'Dividends'])
    gains_df['Total'] = gains_df.sum(1).values
    gains_df['Symbol'] = pf['Symbol']

    return gains_df


def calc_gains_equity(tick, quantity, trade_date, currency, pf, hist, forex):
    """ calc gains separated in intrinsic, dividends and currency-related parts """
    
  #  print(tick, quantity, trade_date, currency)
    # remove data prior to trade date
    rel_equity = hist[hist['Date'] > trade_date][tick]
    
    # do the same for forex if needed
    if currency != 'EUR':
        rel_forex = forex[forex['Date'] > trade_date]['EUR{}=X'.format(currency)]['Close']
    else: # if EUR, dummy re_forex to keep the same code below
        rel_forex = pd.Series([1, 1])
    # intrinsic change
    intrinsic_var = ( rel_equity['Close'].iat[-1] - rel_equity['Close'].iat[0] ) / rel_forex.iat[0] * quantity
    # currency effect
    currency_var = ( 1 / rel_forex.iat[-1] - 1/ rel_forex.iat[0] ) * rel_equity['Close'].iat[-1] * quantity
    
    # dividends
    dividends_var = rel_equity['Dividends'].sum()
    
    return intrinsic_var, currency_var, dividends_var


def tradedate_2_dtime(trade_dates):
    """ batch convert trade date as formatted by yfinance to a datetime object """
    def td2dt(trade_date):
        """ convert single trade date """
        td_str = str(int(trade_date))
        y, m, d = int(td_str[:4]), int(td_str[4:6]), int(td_str[6:])
        return datetime(y, m, d)
    
    return [td2dt(trade_date) for trade_date in trade_dates]

