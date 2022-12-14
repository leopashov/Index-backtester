import pandas as pd
import plotly.express as px

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

def loadBtcData():
    dfBTC = pd.read_csv("../priceHistories/BTCUSD.csv")
    dfBTC['Date'] = pd.to_datetime(dfBTC['Date'])
    # dfBTC.sort_values(by = 'Date', ascending=False, inplace=True)
    dfBTC = dfBTC.rename(columns={'Open':'BTCOpen'})
    dfBTC.set_index('Date', inplace=True)
    return(dfBTC)

def createPricesDataFrame():
    dfEth = loadEthData()['EthOpen']
    dfBTC = loadBtcData()['BTCOpen']

    print(dfEth, dfBTC)

    Prices = pd.concat([dfEth,dfBTC], axis = 1)
    #Prices = pd.merge(dfEth, dfBTC, on = 'Date')
    # Prices.sort_values(by = 'Date', ascending=True, inplace = True)
    return Prices

def main():

    dfPrices = createPricesDataFrame()
    dfPrices.dropna(inplace=True)
    print(dfPrices)
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    REBALANCEFREQ = 1 # how regularly portfolio is balanced, measured in days
    TARGETBTCPROPORTION = 0.5
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    
    # priceFig = px.line(dfPrices, x='Date', y=['EthOpen', 'BTCOpen'], title="Eth and BTC prices")
    # priceFig.show()
    
    dfPrices.at['2015-08-07','EthInPortfolio'] = (1-TARGETBTCPROPORTION)/(dfPrices.at['2015-08-07', "EthOpen"])
    dfPrices.at['2015-08-07','BTCInPortfolio'] = TARGETBTCPROPORTION/(dfPrices.at['2015-08-07', "BTCOpen"])
    dfPrices["EthHODLValue"] = 2 * (dfPrices["EthOpen"]) * (dfPrices.at['2015-08-07', "EthInPortfolio"])
    dfPrices["BTCHODLValue"] = 2 * (dfPrices["BTCOpen"]) * (dfPrices.at['2015-08-07', "BTCInPortfolio"])
    dfPrices["ETH+BTCHODLValue"] = (dfPrices["EthHODLValue"] + dfPrices['BTCHODLValue'])/2
    hodlFig = px.line(dfPrices, x = dfPrices.index, y=['EthHODLValue', 'BTCHODLValue', 'ETH+BTCHODLValue'], title="HODL comparisons")
    hodlFig.show()
    
    
    dfPrices["Eth+Btc EqualWeight"] = 0
    for index, row in enumerate(dfPrices.index):
        if index > 0:
            if index % REBALANCEFREQ == 0:
                # rebalance eth and btc holdings
                BTCDollarValue = dfPrices.at[dfPrices.index[index-1], 'BTCInPortfolio'] * dfPrices.at[dfPrices.index[index], 'BTCOpen']
                EthDollarValue = dfPrices.at[dfPrices.index[index-1], 'EthInPortfolio'] * dfPrices.at[dfPrices.index[index], 'EthOpen']
                portfolioValue = BTCDollarValue + EthDollarValue
                BTCProportion = BTCDollarValue/portfolioValue
                dfPrices.at[dfPrices.index[index], 'BTCInPortfolio'] = dfPrices.at[dfPrices.index[index-1], 'BTCInPortfolio'] - (((BTCProportion-TARGETBTCPROPORTION)*portfolioValue)/dfPrices.at[dfPrices.index[index], 'BTCOpen'])
                dfPrices.at[dfPrices.index[index], 'EthInPortfolio'] = dfPrices.at[dfPrices.index[index-1], 'EthInPortfolio'] + (((BTCProportion-TARGETBTCPROPORTION)*portfolioValue)/dfPrices.at[dfPrices.index[index], 'EthOpen'])
            else:
                dfPrices.at[dfPrices.index[index], 'BTCInPortfolio'] = dfPrices.at[dfPrices.index[index-1], 'BTCInPortfolio']
                dfPrices.at[dfPrices.index[index], 'EthInPortfolio'] = dfPrices.at[dfPrices.index[index-1], 'EthInPortfolio']
    dfPrices['indexValue'] = (dfPrices['EthInPortfolio'] * dfPrices['EthOpen']) + dfPrices['BTCInPortfolio'] * dfPrices['BTCOpen']
    dfPrices['BTCWeight'] = dfPrices['BTCInPortfolio'] * dfPrices['BTCOpen'] / dfPrices['indexValue']
    dfPrices['ETHWeight'] = dfPrices['EthInPortfolio'] * dfPrices['EthOpen'] / dfPrices['indexValue']
    dfPrices['BTCScaledWeight'] = 2000*dfPrices['BTCWeight']

        # print(dfPrices["EthHODLValue"][index])
    print(dfPrices[['BTCInPortfolio', 'EthInPortfolio', 'indexValue', 'BTCWeight', 'ETHWeight']])
    stratFig = px.line(dfPrices, x = dfPrices.index, y=['EthHODLValue', 'BTCHODLValue', 'ETH+BTCHODLValue', 'indexValue', 'BTCScaledWeight'], title="Strategy comparisons")
    stratFig.show()
    dfPrices.to_csv('dataFrame.csv')


if __name__ == "__main__":
    main()