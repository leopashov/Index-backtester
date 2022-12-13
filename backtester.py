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

def writeRemainderOfRow(array, row, prices):
    array[row, 2] = array[row, 0] * prices.ETH[row]
    array[row, 3] = array[row, 1] * prices.BTC[row]
    array[row, 4] = array[row, 3] + array[row, 2]
    array[row, 5] = array[row, 3] / array[row, 4]


def getRebalancedReturns(priceData, targetBtcWeight, rebalanceFrequency):
    # create numpy array of length price data (rows correspond to dates)
    # using numpy as will have to iterate through
    a = np.zeros((len(priceData), 6))
    # Columns: 0.EthHoldings, 1.BtcHoldings, 2.EthUsdValue, 3.BtcUsdVal, 4.TotalValue, 5.BTCProportion
    a[0, 0] = (1-targetBtcWeight) / priceData.ETH[0]
    a[0, 1] = targetBtcWeight / priceData.BTC[0]
    writeRemainderOfRow(a, 0, priceData)

    for i in range(1,len(a)):
        if i % rebalanceFrequency == 0:
            #rebalance
            btcValue = a[i-1, 1] * priceData.BTC[i]
            ethValue = a[i-1, 0] * priceData.ETH[i]
            totalValue = btcValue + ethValue
            btcWeight = btcValue/totalValue
            btcToSell = ((btcWeight-targetBtcWeight)*totalValue)/priceData.BTC[i]
            ethToBuy = ((btcWeight-targetBtcWeight)*totalValue)/priceData.ETH[i]
            a[i, 1] = a[i-1, 1] - btcToSell
            a[i, 0] = a[i-1, 0] + ethToBuy
            writeRemainderOfRow(a, i, priceData)
        else:
            # eth and btc holdings stay same as prev step
            a[i, 0] = a[i-1, 0]
            a[i, 1] = a[i-1, 1]
            writeRemainderOfRow(a, i, priceData)
    # np.savetxt("rebalanced.csv", a, delimiter=",")
    return(a)

def displayFigures(priceData, hold, equalHold, rebal, btcTarget, rebalanceFreq):
    fig1 = px.line(priceData, title="eth-usd and btc-usd price history")
    fig1.show()

    fig2Title = 'returns - BtcWeight: {weight}, rebalance frequency: {freq}'.format(weight = btcTarget, freq = rebalanceFreq)
    print(fig2Title)
    fig2 = px.line(hold, title = fig2Title)
    fig2.add_trace(go.Scatter(x = equalHold.index, y = equalHold, mode="lines", name = '50/50 hold', showlegend = True))
    print(rebal[:, 4])
    fig2.add_trace(go.Scatter(x = equalHold.index, y = rebal[:, 4], mode="lines", name = 'Rebalanced', showlegend = True))
    fig2.show()

    

def main():
    targetBtcWeight = 0.001
    rebalanceFrequency = 90 #days
    prices = createPricesDataFrame()

    holdReturns = getHoldReturns(prices)
    equalHoldReturns = getEqualSplitHoldings(prices, holdReturns)
    rebalArray = getRebalancedReturns(prices, targetBtcWeight, rebalanceFrequency)

    displayFigures(prices, holdReturns, equalHoldReturns, rebalArray, targetBtcWeight, rebalanceFrequency)    


if __name__ == "__main__":
    main()