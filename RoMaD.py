import backtester as bt
import parameterCalculator as pc
import drawdownCalculation as dc
import plotly.graph_objects as go
import pandas as pd

def printSurfacePlot(data, figTitle):
    fig = go.Figure(data=[go.Surface(z=data)])
    fig.update_layout(title = figTitle)
    fig.show()

def main():
    prices = bt.createPricesDataFrame()

    maxReturnsDf = pc.getMaxReturns(prices)
    # print(type(maxReturnsDf))
    absoluteMaxDrawDownsDf = dc.getMaxDailyDrawdownS(prices).abs()
    # print(type(absoluteMaxDrawDownsDf))
    RoMaD = maxReturnsDf.divide(absoluteMaxDrawDownsDf, axis = 'index')
    
    
    
    printSurfacePlot(RoMaD, 'RoMaD for range of rebalance frequencies and weights')




if __name__ == "__main__":
    main()