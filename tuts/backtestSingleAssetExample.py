# XREF https://towardsdatascience.com/backtest-trading-strategies-with-pandas-vectorized-backtesting-26001b0ba3a5

import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import numpy as np

def loadEthData():
    dfEth = pd.read_csv("../priceHistories/ETHUSD.csv")
    dfEth['timestamp'] = pd.to_datetime(dfEth['timestamp'], unit='s') # turn UNIX to datetime
    dfEth['date'] = dfEth['timestamp'].dt.date
    dfEth.drop_duplicates(subset='date', keep='last', inplace=True)
    dfEth.drop('date', axis = 1)
    dfEth = dfEth.rename(columns={'timestamp':'Date','open':'EthOpen'})
    dfEth.sort_values(by = 'Date', ascending=True, inplace=True)
    dfEth.set_index('Date', inplace=True) # set date as dataframe index!
    return(dfEth)

def main():
    prices = loadEthData()['EthOpen']
    print(prices)
    rs = prices.apply(np.log).diff(1) # take log of each price in prices series
    # get the difference between each price
    # ie get log returns
    w1 = 5 # short-term moving average window (5 day)
    w2 = 22 # long-term moving average window (22 day)
    ma_x = prices.rolling(w1).mean() - prices.rolling(w2).mean()

    pos = ma_x.apply(np.sign) # +1 if long, -1 if short

    fig = sp.make_subplots(rows=2, cols=1)
    fig1 = px.line(ma_x)
    fig2 = px.line(pos)
    fig1.show()
    fig2.show()

    my_rs = pos.shift(1)*rs
    fig3 = px.line(my_rs.cumsum().apply(np.exp))
    fig3.show()

if __name__ == "__main__":
    main()