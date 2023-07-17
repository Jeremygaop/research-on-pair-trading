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


futureData = func.combineFutureData('QWF')



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

func.pricePlot(X)
plt.show()