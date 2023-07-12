import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import func

# Load the dir
futureOBDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresOB/"
futureTradeDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresTrades/"
stockDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/stocks/"

colNames = ['date', 'time', 'askPrice5', 'askPrice4', 'askPrice3', 'askPrice2',
       'askPrice1', 'bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4',
       'bidPrice5', 'askSize5', 'askSize4', 'askSize3', 'askSize2', 'askSize1',
       'bidSize1', 'bidSize2', 'bidSize3', 'bidSize4', 'bidSize5', 'symbol']

futureData = func.combineFutureData('QWF')

stoColNames = ['date', 'time', 'lastPx', 'size', 'volume', 'SP5', 'SP4', 'SP3', 'SP2',
       'SP1', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'SV5', 'SV4', 'SV3', 'SV2',
       'SV1', 'BV1', 'BV2', 'BV3', 'BV4', 'BV5']

stockData = func.combineStockData('2388')

commonDays = func.findCommonDay(stockData, futureData)

stockData, futureData = func.indexStockFuture(stockData, futureData, commonDays)

stockData_downsampled = func.syncStock(stockData, futureData)


stockPrice = stockData_downsampled['lastPx']
futurePrice = futureData['midQ']
na_index = stockPrice.isna()
stockPrice = stockPrice[~na_index]
futurePrice = futurePrice[~na_index]
zero_index = (futurePrice == 0)
stockPrice = stockPrice[~zero_index]
futurePrice = futurePrice[~zero_index]

gamma = stockPrice[0] / futurePrice[0]

X = np.log(stockPrice / stockPrice[0]) - gamma * np.log(futurePrice / futurePrice[0])

pricePlot(X)
plt.show()