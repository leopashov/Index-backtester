import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def loadEthData():
    dfEth = pd.read_csv("../priceHistories/ETHUSD.csv")
    dfEth['timestamp'] = pd.to_datetime(dfEth['timestamp'], unit='s') # turn UNIX to datetime
    dfEth['date'] = dfEth['timestamp'].dt.date
    dfEth.drop_duplicates(subset='date', keep='last', inplace=True)
    dfEth.drop('date', axis = 1)
    dfEth = dfEth.rename(columns={'timestamp':'Date','open':'ETH'})
    dfEth.sort_values(by = 'Date', ascending=True, inplace=True)
    dfEth.set_index('Date', inplace=True) # set date as dataframe index!
    return(dfEth)

def loadBtcData():
    dfBTC = pd.read_csv("../priceHistories/BTCUSD.csv")
    dfBTC['Date'] = pd.to_datetime(dfBTC['Date'])
    # dfBTC.sort_values(by = 'Date', ascending=False, inplace=True)
    dfBTC = dfBTC.rename(columns={'Open':'BTC'})
    dfBTC.set_index('Date', inplace=True)
    return(dfBTC)

def createPricesDataFrame():
    dfEth = loadEthData()['ETH']
    dfBTC = loadBtcData()['BTC']
    Prices = pd.concat([dfEth,dfBTC], axis = 1)
    Prices.dropna(inplace=True)
    return Prices

def getHoldReturns(_prices):
    rs = _prices.apply(np.log).diff(1).cumsum().apply(np.exp)
    # take logs of each price and subtract the previous days price to get log returns
    # take a cumulative sum of these before raising to power of e, ending up with 
    # pn/p0 ie return at each point
    return rs

def getEqualSplitHoldings(_prices, holdRs):
    equalSplitHoldings = pd.DataFrame(index=_prices.index)
    equalSplitHoldings = (0.5*holdRs.ETH) + (0.5*holdRs.BTC)
    return equalSplitHoldings


def main():
    prices = createPricesDataFrame()

    fig1 = px.line(prices, title="eth-usd and btc-usd price history")
    fig1.show()

    holdReturns = getHoldReturns(prices)
    equalHoldReturns = getEqualSplitHoldings(prices, holdReturns)
    print(holdReturns)
    fig2 = px.line(holdReturns, title = 'hold returns')
    fig2.add_trace(go.Scatter(x = equalHoldReturns.index, y = equalHoldReturns, mode="lines", name = '50/50 hold', showlegend = True))
    fig2.show()

    


if __name__ == "__main__":
    main()