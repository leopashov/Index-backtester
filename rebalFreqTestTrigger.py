""" The effect of rebalance frequency seemed pretty randome from surface plots - There were many peaks and troughs in close succession and no 'smoothness' unlike the 
effect of btc weight. Here we look to see if there is any correlation between the eth btc chart and the rebalancing frequency which gave the highest returns.
Highets returns were acheived when rebalancing every 136 days"""

import backtester as bt
import backtesterTrigger as btT
import pandas as pd
import plotly.express as px
import datetime
import plotly.graph_objects as go
import numpy as np

def verticalLinePoints(maxValue, date):
    return np.array([[date, 0], [date, maxValue]])

def main():
    prices = bt.createPricesDataFrame()
    # add eth/btc column to prices
    prices['Eth/Btc'] = prices['ETH']/prices['BTC']
    print(prices)

    targetWeight = 0.42
    rebalanceTrigger = 0.41
    # add btc holdings trace
    returns = btT.getRebalancedReturns(prices, targetWeight, rebalanceTrigger)

    fig = px.line(prices, x=prices.index, y=['Eth/Btc'], title = str(f'eth/btc chart with rebalance each {rebalanceTrigger} days'))
    date_1 = prices.index[0]
    for dateIndex in range(0,len(prices), rebalanceTrigger):
        date = date_1 + datetime.timedelta(days=dateIndex)
        points = verticalLinePoints(max(prices['Eth/Btc']), date)
        fig.add_trace(go.Scatter(x = points[:,0], y= points[:, 1]))
    fig.add_trace(go.Scatter(x = prices.index, y= returns[:,1], mode='lines', name='BTC held'))
    fig.show()


if __name__ == "__main__":
    main()