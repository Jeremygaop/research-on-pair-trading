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
futureData_downsampled = func.syncFuture(stockData, futureData)


stockPrice = stockData['price']
futurePrice = futureData_downsampled['midQ']

stockPrice, futurePrice = func.deleZeroNa(stockPrice, futurePrice)


gamma = stockPrice[0] / futurePrice[0]
X = np.log(stockPrice / stockPrice[0]) - gamma * np.log(futurePrice / futurePrice[0])


path = '/Users/shezihua/Downloads/QWF-2388/'
func.path_exists_make(path)


futureData_downsampled.to_csv(path + 'future.csv.gz', compression='gzip', index=False)
stockData.to_csv(path + 'stock.csv.gz', compression='gzip', index=False)
X.to_csv(path + 'spread.csv.gz', compression='gzip', index=False)