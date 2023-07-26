import talib
import pandas as pd


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
