# 
# Created by towshif ali (tali) on 6/30/2018
#

# from pandas_datareader import data
# import matplotlib.pyplot as plt
# import pandas as pd
#
# # Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
# tickers = ['AAPL', 'MSFT', '^GSPC']
#
# # We would like all available data from 01/01/2000 until 12/31/2016.
# start_date = '2010-01-01'
# end_date = '2016-12-31'
#
# # User pandas_reader.data.DataReader to load the desired data. As simple as that.
# panel_data = data.DataReader('INPX', 'google', start_date, end_date)
#
# print (panel_data)

import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from datetime import datetime


yf.pdr_override()
# Set up End and Start times for data grab
end = datetime.now()
# we want the start date to be a year a go
start = datetime(end.year - 1,end.month,end.day)

# let's grab stock data for Apple, Google, Microsoft and Amazon
AAPL = pdr.get_data_yahoo('AAPL', start, end)
GOOG = pdr.get_data_yahoo('GOOG', start, end)
AMZN = pdr.get_data_yahoo('AMZN', start, end)
MSFT = pdr.get_data_yahoo('MSFT', start, end)

# change the Timestamp index in the four data frames to Date
tech_list = [AAPL, GOOG, AMZN, MSFT]

print(AAPL)