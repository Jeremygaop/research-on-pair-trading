import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


# Load the dir
futureOBDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresOB/"
futureTradeDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresTrades/"
stockDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/stocks/"

futurecolNames = ['date', 'time', 'askPrice5', 'askPrice4', 'askPrice3', 'askPrice2',
       'askPrice1', 'bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4',
       'bidPrice5', 'askSize5', 'askSize4', 'askSize3', 'askSize2', 'askSize1',
       'bidSize1', 'bidSize2', 'bidSize3', 'bidSize4', 'bidSize5', 'symbol']

stoColNames = ['date', 'time', 'lastPx', 'size', 'volume', 'SP5', 'SP4', 'SP3', 'SP2',
       'SP1', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'SV5', 'SV4', 'SV3', 'SV2',
       'SV1', 'BV1', 'BV2', 'BV3', 'BV4', 'BV5']

def combineFutureData(name):  # name is the future code, type is string
    futureFileList = []
    for i in os.listdir(futureOBDir + name + "/"):
        futureFileList.append(i)
    # futureFileList.remove('.DS_Store')
    futureFileList = sorted(futureFileList)
    futureData = pd.DataFrame([], columns=futurecolNames)
    for file in futureFileList:
        if file[-1] == 'v':
            futureOB_data = pd.read_csv(futureOBDir + name + '/' + file)
        else: 
            futureOB_data = pd.read_csv(futureOBDir + name + '/' + file, compression='gzip')
        futureData = pd.concat([futureData, futureOB_data])
        futureData = futureData.reset_index(drop=True)
        futureData['midQ'] = ((futureData['askPrice1'] + futureData['bidPrice1']) / 2).astype(float)
    return futureData

def pricePlot(data):
    plt.figure(figsize=(20,10))
    plt.plot(data)



def combineStockData(name):
    stockFileList = []
    for i in os.listdir(stockDir + name + "/"):
        stockFileList.append(i)
    # stockFileList.remove('.DS_Store')
    stockFileList = sorted(stockFileList)
    stockData = pd.DataFrame([], columns=stoColNames)
    for file in stockFileList:
        stock_data = pd.read_csv(stockDir + name + '/' + file, compression='gzip', index_col=0)
        stockData = pd.concat([stockData, stock_data])
    stockData = stockData.reset_index(drop=True)
    return stockData


def findCommonDay(stockData, futureData):
    stockData_dates = np.unique(stockData.date)
    stoD = pd.to_datetime(stockData_dates, format="%Y-%m-%d")
    qqqq = stoD.year * 10000 + stoD.month * 100 + stoD.day
    futureData_dates = np.unique(futureData.date)
    indD = pd.to_datetime(futureData_dates, format="%Y-%m-%d")
    pppp = indD.year * 10000 + indD.month * 100 + indD.day
    commonDays = pd.to_datetime(pppp.intersection(qqqq),format="%Y%m%d")
    return commonDays


def indexStockFuture(stockData, futureData, commonDays):
    ## With common days generated for both stock and futures, we synchronize days first
    d_futures = pd.to_datetime(futureData.date, format="%Y-%m-%d")
    futureData.date = d_futures
    futureData = futureData[futureData.date.isin(commonDays)]

    d_stock = pd.to_datetime(stockData.date, format="%Y-%m-%d")
    stockData.date = d_stock
    stockData = stockData[stockData.date.isin(commonDays)]

    ## In order to synchronize trade time, too, we create indexes for both dataframes that have the same format
    stockData_DateTime = pd.to_datetime(stockData.date.astype(str) + ' ' + stockData.time.astype(str), format="%Y-%m-%d %H%M%S%f")
    futuresData_DateTime = pd.to_datetime(futureData.date.astype(str) + ' ' + futureData.time.astype(str), format="%Y-%m-%d %H%M%S%f")

    stockData.index = stockData_DateTime
    stockData = stockData[~stockData.index.duplicated(keep='last')]   

    futureData.index = futuresData_DateTime
    futureData = futureData[~futureData.index.duplicated(keep='last')]
    return stockData, futureData


def syncStock(stockData, futureData):
    ## Now, we synchronize the timestamps of the two time series; here, we downsample the time series with more time stamps
    ### First, we union the indexes
    new_index1 = stockData.index.union(futureData.index)
    new_index = np.unique(new_index1)

    ### Next, we insert stock time stamps to index futures data
    resampledStockData = stockData.reindex(new_index)

    ### Then, we forward fill nan's in the index futures data so that date and time will not be nan's
    resampledStockData.fillna(method='ffill',inplace=True)
    stockData_downsampled = resampledStockData.loc[futureData.index]
    return stockData_downsampled





