import backtesterTrigger as btT
import backtester as bt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import signal

def getMaxReturns(priceData):
    weightsRange = np.arange(0,1.01,0.01)
    triggerRange = np.arange(0,0.5,0.01)
    runs = len(triggerRange) * len(weightsRange)
    maxReturns = pd.DataFrame(index = triggerRange, columns = weightsRange)
    # maxReturns = np.zeros(len(weightsRange)*len(triggerRange),3)
    i = 0
    for rebalanceFrequency in triggerRange:
        for targetBtcWeight in weightsRange:
            maxReturns.at[rebalanceFrequency,targetBtcWeight] = btT.getRebalancedReturns(priceData, targetBtcWeight, rebalanceFrequency)[:, 4].max()
            print(f'completed: ',i,'of', runs, 'calculations')
            i+=1
    maxReturns.to_pickle("./maxReturnsTrigger")
    return maxReturns

def getPeaksAndTroughs(priceData, targetBtcWeight, rebalanceFrequency):
    # get peaks and troughs of one sim (1 set of weighting and rebal frequency)
    rets = btT.getRebalancedReturns(priceData, targetBtcWeight, rebalanceFrequency)[:, 4]
    peaks = signal.find_peaks(rets)
    print(peaks)
    troughs = signal.find_peaks(-rets)
    print(troughs)

def printMaxReturnsSurfacePlot(maxReturnsDf):
    fig = go.Figure(data=[go.Surface(z=maxReturnsDf)])
    fig.update_layout(title = 'max returns, weight and rebalance frequency variables')
    fig.show()



def main():
    prices = bt.createPricesDataFrame()

    # print(prices)
    
    # rebalTotVals = bt.getRebalancedReturns(prices, targetBtcWeight, rebalanceFrequency)[:, 4]
    maxReturnsDf = getMaxReturns(prices)
    printMaxReturnsSurfacePlot(maxReturnsDf)

    # getPeaksAndTroughs(prices, 0.43, 137)

if __name__ == "__main__":
    main()