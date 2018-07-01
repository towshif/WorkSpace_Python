# 
# Created by towshif ali (tali) on 6/30/2018
#

import pandas as pd
from pandas_datareader import data as pdr
from stockstats import StockDataFrame as Sdf
import fix_yahoo_finance as yf
from datetime import datetime
from datetime import timedelta
#
# yf.pdr_override()
# end = datetime.now()
# # we want the start date to be a year a go
# start = datetime(end.year,end.month-3,end.day)
# # AAPL = pdr.get_data_yahoo('AAPL', start, end)
# # GOOG = pdr.get_data_yahoo('GOOG', start, end)
# # AMZN = pdr.get_data_yahoo('AMZN', start, end)
# # MSFT = pdr.get_data_yahoo('MSFT', start, end)
# ASML = pdr.get_data_yahoo('ASML', start, end)
#
# data = ASML
#
# print data



#  MACD / SIGNAL INDICATOR CALCULATOR

csv_data = pd.read_csv('stock_data/ASML.csv')
# convert date col to datetime
csv_data['Date'] = pd.to_datetime(csv_data['Date'])
end = datetime.now()
start = datetime(end.year,end.month,end.day) - timedelta(days=180)
data = csv_data[(csv_data['Date'] >= start)]

stock  = Sdf.retype(data)

rsi = stock ['rsi_6']
vr = stock ['vr']

sto1 = stock['kdjk']
sto2 = stock['kdjd']
sto3 = stock['kdjj']


signal = stock['macds']        # Your signal line
macd   = stock['macd']         # The MACD that need to cross the signal line
#                                              to give you a Buy/Sell signal
listLongShort = ["No data"]    # Since you need at least two days in the for loop

macd_ind = [0]

for i in range(1, len(signal)):
    #                          # If the MACD crosses the signal line upward
    if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
        listLongShort.append("BUY")
        # macd_ind.append(-macd[i-1])
        macd_ind.append(1)
    #                          # The other way around
    elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
        listLongShort.append("SELL")
        # macd_ind.append(macd[i-1])
        macd_ind.append(-1)
    #                          # Do nothing if not crossed
    else:
        listLongShort.append("HOLD")
        macd_ind.append(0)

stock['macd_ind'] = macd_ind
stock['Advice'] = listLongShort

# The advice column means "Buy/Sell/Hold" at the end of this day or
#  at the beginning of the next day, since the market will be closed

print(stock['Advice'])

import matplotlib.pyplot as plt

# plt.plot(AAPL, c='r')
# plt.legend(['AAPL'])
# plt.show()


plt.plot( sto1, c='black')
plt.plot( sto2, c='red')
plt.plot( sto3, c='y')
plt.legend(['stok', 'stod', 'stoj'])
plt.show()

plt.plot(signal, c='r')
# plt.show()
plt.plot(macd, c='b')
plt.plot(stock['macd_ind'],c='lime')
plt.legend (['signal', 'macd', 'E-index'])
plt.plot()
plt.show()

plt.plot(rsi, c='c')
plt.legend (['RSI: relative strength index'])
plt.show()
plt.plot(vr, c='y')
plt.legend (['volatility-vol ratio'])
plt.show()

# stocks = pd.DataFrame({"AAPL": AAPL['Close'],
#                        "MSFT": MSFT['Close'],
#                        "GOOG": GOOG['Close']})
# # stocks.head()
# plt.plot(stocks)
# plt.show()
# stocks.plot(secondary_y = ["AAPL", "MSFT"], grid = True)