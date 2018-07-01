# 
# Created by towshif ali (tali) on 6/30/2018
#

import pandas as pd
from pandas_datareader import data as pdr
from stockstats import StockDataFrame as Sdf
import fix_yahoo_finance as yf
from datetime import datetime
from datetime import timedelta

yf.pdr_override()
end = datetime.now()
# we want the start date to be a year a go
start = datetime(end.year,end.month,end.day) - timedelta(days=365)
ticker = ['AAPL', 'GOOG', 'AMZN', 'MSFT', 'ASML', 'AMAT', 'KLAC', 'LRCX', 'FB']

# for tick in ticker:
#     tick_data = pdr.get_data_yahoo(tick, start, end)
#     tick_data.to_csv('stock_data/' +tick+ '.csv')

# AAPL = pdr.get_data_yahoo('AAPL', start, end)
# # GOOG = pdr.get_data_yahoo('GOOG', start, end)
# # AMZN = pdr.get_data_yahoo('AMZN', start, end)
# # MSFT = pdr.get_data_yahoo('MSFT', start, end)
# ASML = pdr.get_data_yahoo('ASML', start, end)
# # data = pdr.get_data_robinhood('AAPL', start, end)
# stk = AAPL
# AAPL.to_csv('stock_data/'+'.csv')


# import pandas_datareader as web
# df = web.data.get_data_yahoo('AAPL', start, end)
# df.to_csv('AAPL-2.csv')
# print df

# Minutes Data interval

# Uncomment below line to install alpha_vantage
#!pip install alpha_vantage
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

import matplotlib.pyplot as plt
ts = TimeSeries(key='BIDI11IT2BK93DEO', output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')

ti = TechIndicators(key='BIDI11IT2BK93DEO', output_format='pandas')
data, meta_data = ti.get_macd(symbol='MSFT', interval='60min')

data, meta_data = ti.get_stoch( symbol='MSFT', interval='60min')
# data, meta_data = ti.get_stochrsi(symbol='MSFT', interval='30min')

print(data.tail())
# data['4. close'].plot()
data.plot()
print ( len(data) )
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()