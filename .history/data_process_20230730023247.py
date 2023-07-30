import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import func


print("Data process Begin")

# Load the dir
futureOBDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresOB/"
futureTradeDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresTrades/"
stockDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/stocks/"
print("dir loading finished")


futureCodeList = ['JBF', 'QWF', 'HCF', 'DBF', 'EHF', 'IPF', 'IIF', 'QXF', 'PEF', 'NAF']
stockCodeList = ['3443', '2388', '2498', '2610', '1319', '3035', '3006', '2615', '5425', '3105']


for i in range(10):
    futureCode = futureCodeList[i]
    stockCode = stockCodeList[i]
    print(futureCode + '-' + stockCode + " pairs begin")

    futureData = func.combineFutureData(futureCode)
    stockData = func.combineStockData(stockCode)
    print("data combination finished")

    commonDays = func.findCommonDay(stockData, futureData)
    stockData, futureData = func.indexStockFuture(stockData, futureData, commonDays)
    futureData_downsampled = func.syncFuture(stockData, futureData)
    print("futrue data downsample finished")


    stockPrice = stockData['price']
    futurePrice = futureData_downsampled['midQ']
    stockPrice, futurePrice = func.deleZeroNa(stockPrice, futurePrice)
    print("price calculation finished")


    gamma = stockPrice[0] / futurePrice[0]
    X = np.log(stockPrice / stockPrice[0]) - gamma * np.log(futurePrice / futurePrice[0])
    print("spread calculation finished")


    path = '/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/SummerIndependentProject/dataCleaned/' + futureCode + '-' + stockCode + '/'
    func.path_exists_make(path)


    futureData_downsampled.to_csv(path + 'future.csv.gz', compression='gzip', index=True)
    print("future data saving finished")
    stockData.to_csv(path + 'stock.csv.gz', compression='gzip', index=True)
    print("stock data saving finished")
    X.to_csv(path + 'spread.csv.gz', compression='gzip', index=True)
    print("spread data saving finished")
    print(futureCode + '-' + stockCode + " pairs finish")
    print("=================")

print("All data process are finished")