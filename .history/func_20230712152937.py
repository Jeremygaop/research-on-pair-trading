import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

%matplotlib inline

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
    return futureData

    