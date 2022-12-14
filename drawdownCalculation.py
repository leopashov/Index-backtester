import backtester as bt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def showMaxDailyDrawdownGraph(priceData, maxDrawdown):
    fig = px.line(maxDrawdown, x = priceData.index, y = maxDrawdown, title = 'max daily drawdown')
    fig.show()


def getMaxDailyDrawdown(priceData, targetBtcWeight, rebalanceFrequency):
    indexValue = bt.getRebalancedReturns(priceData, targetBtcWeight, rebalanceFrequency)[:, 4]
    Roll_Max = np.maximum.accumulate(indexValue)
    Daily_Drawdown = indexValue/Roll_Max - 1.0
    Max_Daily_Drawdown = np.minimum.accumulate(Daily_Drawdown)
    # showMaxDailyDrawdownGraph(priceData, Max_Daily_Drawdown)
    return Max_Daily_Drawdown.min()

def getMaxDailyDrawdownS(priceData):
    weightsRange = np.arange(0,1.01,0.01)
    freqRange = range(1,367,5)
    runs = len(freqRange) * len(weightsRange)
    maxDailyDrawdowns = pd.DataFrame(index = freqRange, columns = weightsRange)
    i = 0
    for rebalanceFrequency in freqRange:
        for targetBtcWeight in weightsRange:
            maxDailyDrawdowns.at[rebalanceFrequency,targetBtcWeight] = getMaxDailyDrawdown(priceData, targetBtcWeight, rebalanceFrequency)
            print(f'completed: ',i,'of', runs, 'calculations')
            i+=1
    return maxDailyDrawdowns

def printMaxDrawdownSurfacePlot(maxDrawdownsDf):
    fig = go.Figure(data=[go.Surface(z=maxDrawdownsDf)])
    fig.update_layout(title = 'max drawdowns, weight and rebalance frequency variables')
    fig.show()


def main():
    prices = bt.createPricesDataFrame()
    printMaxDrawdownSurfacePlot(getMaxDailyDrawdownS(prices))


if __name__ == "__main__":
    main()