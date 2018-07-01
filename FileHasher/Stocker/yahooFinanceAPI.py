# 
# Created by towshif ali (tali) on 6/30/2018
#

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd


# import pandas_datareader.data as web
# import datetime
# start = datetime.datetime(2015, 1, 1)
# end = datetime.datetime(2015, 1, 27)
# # f = web.DataReader('F', 'google', start, end)
# f = web.DataReader('F', 'iex', start, end)
# print (f)
# f.ix['2015-01-08']

import fix_yahoo_finance as yf
# yf.pdr_override() # <== that's all it takes :-)

data = yf.download("SPY", start="2017-01-01", end="2017-04-30")
print ("finance.yahoo.com")
print (data)
# data = pdr.get_data_yahoo(["SPY", "IWM"], start="2017-01-01", end="2017-04-30")
# print (data)



# from pandas_datareader import data as pdr
# import fix_yahoo_finance as yf
# yf.pdr_override() # <== that's all it takes :-)
# # data = pdr.get_data_yahoo('APPL', start='2017-04-23', end='2017-05-24')
# data = yf.download("APPL", start="2017-01-01", end="2017-04-30")
# print (data)