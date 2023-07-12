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