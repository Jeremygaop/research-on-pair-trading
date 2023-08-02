import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import func


print("Factor Building Begin")
print("=======================")


futureCodeList = ['JBF', 'QWF', 'HCF', 'DBF', 'EHF', 'IPF', 'IIF', 'QXF', 'PEF', 'NAF']
stockCodeList = ['3443', '2388', '2498', '2610', '1319', '3035', '3006', '2615', '5425', '3105']

for i in range(len(futureCodeList)):
    futureCode = futureCodeList[i]
    stockCode = stockCodeList[i]
    print(futureCode + '-' + stockCode + " pairs begin")

    print("Data loading begin")
    stock = pd.read_csv("/Users/shezihua/Downloads/" + futureCode + "-" + stockCode + "/stock.csv.gz", compression='gzip', index_col=0)
    future = pd.read_csv("/Users/shezihua/Downloads/" + futureCode + "-" + stockCode + "/future.csv.gz", compression='gzip', index_col=0)
    spread = pd.read_csv("/Users/shezihua/Downloads/" + futureCode + "-" + stockCode + "/spread.csv.gz", compression='gzip', index_col=0, names=['spread'])
    spread = spread.drop(index=[spread.index[0]])
    print("Data loading finished")

    feature = pd.DataFrame()
    feature = func.get_factor(feature, spread, future, stock)
    print("Feature building finished")

    feature = feature.fillna(value=0)
    feature.index = pd.to_datetime(feature.index)
    # corr_table = feature.corr()
    # corr_table.style.background_gradient(cmap='coolwarm')

    factor_path = '/Users/shezihua/Documents/MAFM/2022-2023 Summer/MAFS 6100L/SummerIndependentProject/factor/' + futureCode + '-' + stockCode + '/'
    func.path_exists_make(factor_path)
    feature.to_csv(factor_path + 'factor.csv.gz', compression='gzip', index=True)
    print(futureCode + "-" + stockCode + "Factor buiding finished")
    print("=======================")

