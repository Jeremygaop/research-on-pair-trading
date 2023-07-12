import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


# Load the dir
futureOBDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresOB/"
futureTradeDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/futuresTrades/"
stockDir = "/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/Hongsong CHOU/data/stocks/"

colNames = ['date', 'time', 'askPrice5', 'askPrice4', 'askPrice3', 'askPrice2',
       'askPrice1', 'bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4',
       'bidPrice5', 'askSize5', 'askSize4', 'askSize3', 'askSize2', 'askSize1',
       'bidSize1', 'bidSize2', 'bidSize3', 'bidSize4', 'bidSize5', 'symbol']

def combineFutureData(name):  # name is the future code, type is string
    futureFileList = []
    for i in os.listdir(futureOBDir + name + "/"):
        futureFileList.append(i)
    # futureFileList.remove('.DS_Store')
    futureFileList = sorted(futureFileList)
    futureData = pd.DataFrame([], columns=colNames)
    for file in futureFileList:
        if file[-1] == 'v':
            futureOB_data = pd.read_csv(futureOBDir + name + '/' + file)
        else: 
            futureOB_data = pd.read_csv(futureOBDir + name + '/' + file, compression='gzip')
        futureData = pd.concat([futureData, futureOB_data])
        futureData = futureData.reset_index(drop=True)
        futureData['midQ'] = ((futureData['askPrice1'] + futureData['bidPrice1']) / 2).astype(float)
    return futureData

