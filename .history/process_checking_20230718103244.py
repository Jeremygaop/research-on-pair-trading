import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import func
import os
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.ar_model import AutoReg

futureCodeList = ['JBF', 'QWF', 'HCF', 'DBF', 'EHF', 'IPF', 'IIF', 'QXF', 'PEF', 'NAF']
stockCodeList = ['3443', '2388', '2498', '2610', '1319', '3035', '3006', '2615', '5425', '3105']

maindir = os.getcwd()

for i in range(10):
    futureCode = futureCodeList[i]
    stockCode = stockCodeList[i]

    print(futureCode + '-' + stockCode + " spread test")
    X = pd.read_csv(maindir + '/dataCleaned/' + futureCode + '-' + stockCode + '/spread.csv.gz', compression='gzip')
    func.pricePlot(X)
    plt.title(futureCode + '-' + stockCode + " spread")
    plt.show()

    pacf = plot_pacf(X, lags=10)
    plt.title("PACF of spread")
    pacf.show()

    model = AutoReg(X, lags=1).fit()
    pacf = plot_pacf(model.resid, lags=10)
    plt.title("PACF of residual")
    pacf.show()
    print("=======================")