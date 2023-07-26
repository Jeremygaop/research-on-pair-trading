import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


# Load the dir
futureOBDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresOB/"
futureTradeDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresTrades/"
stockDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/stocks/"


def combineFutureData(name):  # name is the future code, type is string
    futurecolNames = ['date', 'time', 'askPrice5', 'askPrice4', 'askPrice3', 'askPrice2',
       'askPrice1', 'bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4',
       'bidPrice5', 'askSize5', 'askSize4', 'askSize3', 'askSize2', 'askSize1',
       'bidSize1', 'bidSize2', 'bidSize3', 'bidSize4', 'bidSize5', 'symbol']
    futureFileList = []
    for i in os.listdir(futureOBDir + name + "/"):
        futureFileList.append(i)
    if '.DS_Store' in futureFileList:
        futureFileList.remove('.DS_Store')
    futureFileList = sorted(futureFileList)
    futureData = pd.DataFrame([], columns=futurecolNames)
    for file in futureFileList:
        if file[-1] == 'v':
            futureOB_data = pd.read_csv(futureOBDir + name + '/' + file)
        else: 
            futureOB_data = pd.read_csv(futureOBDir + name + '/' + file, compression='gzip')
        futureData = pd.concat([futureData, futureOB_data])
        futureData = futureData.drop(futureData.askPrice1[futureData.askPrice1 == 0].index)
        futureData = futureData.drop(futureData.bidPrice1[futureData.bidPrice1 == 0].index)
        futureData = futureData.reset_index(drop=True)
        futureData['midQ'] = ((futureData['askPrice1'] + futureData['bidPrice1']) / 2).astype(float)
    return futureData

def pricePlot(data):
    plt.figure(figsize=(20,10))
    plt.plot(data)



def combineStockData(name):
    stoColNames = ['date', 'time', 'lastPx', 'size', 'volume', 'SP5', 'SP4', 'SP3', 'SP2',
       'SP1', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'SV5', 'SV4', 'SV3', 'SV2',
       'SV1', 'BV1', 'BV2', 'BV3', 'BV4', 'BV5']
    stockFileList = []
    for i in os.listdir(stockDir + name + "/"):
        stockFileList.append(i)
    # stockFileList.remove('.DS_Store')
    stockFileList = sorted(stockFileList)
    stockData = pd.DataFrame([], columns=stoColNames)
    for file in stockFileList:
        stock_data = pd.read_csv(stockDir + name + '/' + file, compression='gzip', index_col=0)
        stockData = pd.concat([stockData, stock_data])
    stockData = stockData.drop(stockData.SP1[stockData.SP1 == 0].index)
    stockData = stockData.drop(stockData.BP1[stockData.BP1 == 0].index)
    stockData['price'] = ((stockData['SP1'] + stockData['BP1'])/2).astype(float)
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

def deleZeroNa(stockPrice, futurePrice):
    na_index = stockPrice.isna()
    stockPrice = stockPrice[~na_index]
    futurePrice = futurePrice[~na_index]
    na_index = futurePrice.isna()
    stockPrice = stockPrice[~na_index]
    futurePrice = futurePrice[~na_index]
    zero_index = (futurePrice == 0.0)
    stockPrice = stockPrice[~zero_index]
    futurePrice = futurePrice[~zero_index]
    zero_index = (stockPrice == 0.0)
    stockPrice = stockPrice[~zero_index]
    futurePrice = futurePrice[~zero_index]
    return stockPrice, futurePrice


def syncFuture(stockData, futureData):
    ## Now, we synchronize the timestamps of the two time series; here, we downsample the time series with more time stamps
    ### First, we union the indexes
    new_index1 = stockData.index.union(futureData.index)
    new_index = np.unique(new_index1)

    ### Next, we insert stock time stamps to index futures data
    resampledFutureData = futureData.reindex(new_index)

    ### Then, we forward fill nan's in the index futures data so that date and time will not be nan's
    resampledFutureData.fillna(method='ffill',inplace=True)
    futureData_downsampled = resampledFutureData.loc[stockData.index]
    return futureData_downsampled


def path_exists_make(path):
    # path: 需要判断的路径
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def get_all_price_volume_factors(price_df):
    # calculate the moving average
    price_df['MA_5'] = talib.SMA(price_df['spread'], timeperiod=5)
    price_df['MA_20'] = talib.SMA(price_df['spread'], timeperiod=20)
    price_df['MA_60'] = talib.SMA(price_df['spread'], timeperiod=60)

    # calculate the moving average convergence divergence
    price_df['MACD'], price_df['MACDsignal'], price_df['MACDhist'] = talib.MACD(price_df['spread'], fastperiod=12, slowperiod=26, signalperiod=9)

    # calculate the relative strength index
    price_df['RSI'] = talib.RSI(price_df['spread'], timeperiod=14)

    # calculate EMA
    price_df['EMA_5'] = talib.EMA(price_df['spread'], timeperiod=5)
    price_df['EMA_20'] = talib.EMA(price_df['spread'], timeperiod=20)
    price_df['EMA_60'] = talib.EMA(price_df['spread'], timeperiod=60)

    # calculate time to the end of the day,t the end of the day is 13:25
    time_left = (pd.to_datetime('13:25:00') - pd.to_datetime(price_df.index.time, format='%H:%M:%S')).seconds
    total_time = (pd.to_datetime('13:25:00')-pd.to_datetime('09:00:00')).seconds
    price_df['time_to_end'] = time_left/total_time

    return price_df
