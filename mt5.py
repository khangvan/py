from IPython.core.interactiveshell import InteractiveShell

# pretty print all cell's output and not just the last one
# InteractiveShell.ast_node_interactivity = "all"
# pretty print only the last output of the cell
InteractiveShell.ast_node_interactivity = "last_expr"

# def importlib():
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os

import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

from datetime import datetime, timedelta
from datetime import datetime
import time
import pytz    
import html
import qgrid
import talib
import copy

import pdvega  # adds vgplot attribute to pandas

import altair as alt
from vega_datasets import data

import pickle

# importlib()
from MetaTrader5 import *
from datetime import datetime
import pandas as pd
# function call data from multiframe


def convertTimezone(inputdatetime):
#     utc_time = datetime.utcnow()
    utc_time=inputdatetime
    tz = pytz.timezone('America/Los_Angeles')

    utc_time =utc_time.replace(tzinfo=pytz.UTC) #replace method      
    st_john_time=utc_time.astimezone(tz)        #astimezone method
#     print(st_john_time)
    return st_john_time

print("current time is %s"%convertTimezone(datetime.now()))

def getMT5data(pair="EURUSD",timeframe=MT5_TIMEFRAME_M1, point=5000):
   
    import pandas as pd
    # Initializing MT5 connection 
    MT5Initialize()
    MT5WaitForTerminal()

#     print(MT5TerminalInfo())
#     print(MT5Version())

    # Copying data to pandas data frame
    stockdata = pd.DataFrame()
    # rates = MT5CopyRatesFromPos("EURUSD", MT5_TIMEFRAME_M1, 0, 5000)
    rates = MT5CopyRatesFromPos(pair, timeframe, 0, point)
    # Deinitializing MT5 connection
    MT5Shutdown()

    stockdata['Open'] = [y.open for y in rates]
    stockdata['Close'] = [y.close for y in rates]
    stockdata['High'] = [y.high for y in rates]
    stockdata['Low'] = [y.low for y in rates]
    stockdata['Date'] = [y.time for y in rates]
    stockdata['Vol'] = [y.tick_volume for y in rates]
    import plotly.graph_objs as go
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


    trace = go.Ohlc(x=stockdata['Date'],
                    open=stockdata['Open'],
                    high=stockdata['High'],
                    low=stockdata['Low'],
                    close=stockdata['Close'])
    


    # data = [trace]
    # # plot(data)
    df=stockdata
    
                # get UTC offset for the local PC
    UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()

    # create a simple function correcting the offset head-on
    def local_to_utc(dt):
#         return dt + UTC_OFFSET_TIMEDELTA
#         return(dt-timedelta(hours=3)) # hinh nhu my
        return dt-timedelta(hours=2) # từ vietnam

    # apply the offset for the 'time' column in the rates_frame dataframe
    df['Date'] = df.apply(lambda df: local_to_utc(df['Date']), axis=1)
    
#     def getworkday(df):
#         excluded=(6,7)
#         d=df['Date'].values
#         rs=""
#         if d.isoweekday() not in excluded:
#             rs= 'w'
#         else: 
#             rs= 'o'
#         return rs
        
#     df['Day'] =df.apply(lambda x: getworkday, axis=1)
    
#     print(df["Date"].max())
    #y value
    #Build Update data cleaning
#     n=1
#     df.loc[df.Close.shift(-n)>df.Close,'y']=1
#     df.loc[df.Close.shift(-n)<df.Close,'y']=-1
#     df.loc[df.Close.shift(-n)==df.Close,'y']=0
    
    # richer data
    df= richerTablib(df)
#     df= richerBB(df)
    #bbrange 
    df=richerBB(df)
    
#     df.dropna(inplace=True)
#     print("dropped NA last record")
    
    df['PipValue']=(df.Close.shift(1)-df.Close)*100000
    df["frame"]= str(timeframe)
    df.sort_values(by='Date', ascending=True)
    return df
def richerBB(df):
    from talib import MA_Type
    
    # print(df.count())
    
    df["upperband_2h"], df["middleband_2m"], df["lowerband_2l"] = talib.BBANDS(df.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df["upperband_1h"], df["middleband_1m"], df["lowerband_1l"] = talib.BBANDS(df.Close, timeperiod=20, nbdevup=1, nbdevdn=1, matype=0)
    # df.head(100)
    def bbrange(row):
        value=0
        if (row['Close'] >=row['upperband_1h'] and row['Close'] <=row['upperband_2h'] ):
            value = +1
        elif (row['Close'] <=row['lowerband_1l'] and row['Close'] >=row['lowerband_2l']):
            value = -1
        return value
    #create bbrange
    df['CDLbbrange']=df.apply(bbrange,axis=1)
    df.drop(columns=['upperband_2h','middleband_2m','lowerband_2l','upperband_1h','middleband_1m','lowerband_1l'],inplace=True)
    
    return df
def richerTablib(df):
    df['CDL2CROWS']=talib.CDL2CROWS(df.Open,df.High,df.Low,df.Close)
    df['CDL3BLACKCROWS']=talib.CDL3BLACKCROWS(df.Open,df.High,df.Low,df.Close)
    df['CDL3INSIDE']=talib.CDL3INSIDE(df.Open,df.High,df.Low,df.Close)
    df['CDL3LINESTRIKE']=talib.CDL3LINESTRIKE(df.Open,df.High,df.Low,df.Close)
    df['CDL3OUTSIDE']=talib.CDL3OUTSIDE(df.Open,df.High,df.Low,df.Close)
    df['CDL3STARSINSOUTH']=talib.CDL3STARSINSOUTH(df.Open,df.High,df.Low,df.Close)
    df['CDL3WHITESOLDIERS']=talib.CDL3WHITESOLDIERS(df.Open,df.High,df.Low,df.Close)
    df['CDLABANDONEDBABY']=talib.CDLABANDONEDBABY(df.Open,df.High,df.Low,df.Close)
    df['CDLADVANCEBLOCK']=talib.CDLADVANCEBLOCK(df.Open,df.High,df.Low,df.Close)
    df['CDLBELTHOLD']=talib.CDLBELTHOLD(df.Open,df.High,df.Low,df.Close)
    df['CDLBREAKAWAY']=talib.CDLBREAKAWAY(df.Open,df.High,df.Low,df.Close)
    df['CDLCLOSINGMARUBOZU']=talib.CDLCLOSINGMARUBOZU(df.Open,df.High,df.Low,df.Close)
    df['CDLCONCEALBABYSWALL']=talib.CDLCONCEALBABYSWALL(df.Open,df.High,df.Low,df.Close)
    df['CDLCOUNTERATTACK']=talib.CDLCOUNTERATTACK(df.Open,df.High,df.Low,df.Close)
    df['CDLDARKCLOUDCOVER']=talib.CDLDARKCLOUDCOVER(df.Open,df.High,df.Low,df.Close)
    df['CDLDOJI']=talib.CDLDOJI(df.Open,df.High,df.Low,df.Close)
    df['CDLDOJISTAR']=talib.CDLDOJISTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLDRAGONFLYDOJI']=talib.CDLDRAGONFLYDOJI(df.Open,df.High,df.Low,df.Close)
    df['CDLENGULFING']=talib.CDLENGULFING(df.Open,df.High,df.Low,df.Close)
    df['CDLEVENINGDOJISTAR']=talib.CDLEVENINGDOJISTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLEVENINGSTAR']=talib.CDLEVENINGSTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLGAPSIDESIDEWHITE']=talib.CDLGAPSIDESIDEWHITE(df.Open,df.High,df.Low,df.Close)
    df['CDLGRAVESTONEDOJI']=talib.CDLGRAVESTONEDOJI(df.Open,df.High,df.Low,df.Close)
    df['CDLHAMMER']=talib.CDLHAMMER(df.Open,df.High,df.Low,df.Close)
    df['CDLHANGINGMAN']=talib.CDLHANGINGMAN(df.Open,df.High,df.Low,df.Close)
    df['CDLHARAMI']=talib.CDLHARAMI(df.Open,df.High,df.Low,df.Close)
    df['CDLHARAMICROSS']=talib.CDLHARAMICROSS(df.Open,df.High,df.Low,df.Close)
    df['CDLHIGHWAVE']=talib.CDLHIGHWAVE(df.Open,df.High,df.Low,df.Close)
    df['CDLHIKKAKE']=talib.CDLHIKKAKE(df.Open,df.High,df.Low,df.Close)
    df['CDLHIKKAKEMOD']=talib.CDLHIKKAKEMOD(df.Open,df.High,df.Low,df.Close)
    df['CDLHOMINGPIGEON']=talib.CDLHOMINGPIGEON(df.Open,df.High,df.Low,df.Close)
    df['CDLIDENTICAL3CROWS']=talib.CDLIDENTICAL3CROWS(df.Open,df.High,df.Low,df.Close)
    df['CDLINNECK']=talib.CDLINNECK(df.Open,df.High,df.Low,df.Close)
    df['CDLINVERTEDHAMMER']=talib.CDLINVERTEDHAMMER(df.Open,df.High,df.Low,df.Close)
    df['CDLKICKING']=talib.CDLKICKING(df.Open,df.High,df.Low,df.Close)
    df['CDLKICKINGBYLENGTH']=talib.CDLKICKINGBYLENGTH(df.Open,df.High,df.Low,df.Close)
    df['CDLLADDERBOTTOM']=talib.CDLLADDERBOTTOM(df.Open,df.High,df.Low,df.Close)
    df['CDLLONGLEGGEDDOJI']=talib.CDLLONGLEGGEDDOJI(df.Open,df.High,df.Low,df.Close)
    df['CDLLONGLINE']=talib.CDLLONGLINE(df.Open,df.High,df.Low,df.Close)
    df['CDLMARUBOZU']=talib.CDLMARUBOZU(df.Open,df.High,df.Low,df.Close)
    df['CDLMATCHINGLOW']=talib.CDLMATCHINGLOW(df.Open,df.High,df.Low,df.Close)
    df['CDLMATHOLD']=talib.CDLMATHOLD(df.Open,df.High,df.Low,df.Close)
    df['CDLMORNINGDOJISTAR']=talib.CDLMORNINGDOJISTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLMORNINGSTAR']=talib.CDLMORNINGSTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLONNECK']=talib.CDLONNECK(df.Open,df.High,df.Low,df.Close)
    df['CDLPIERCING']=talib.CDLPIERCING(df.Open,df.High,df.Low,df.Close)
    df['CDLRICKSHAWMAN']=talib.CDLRICKSHAWMAN(df.Open,df.High,df.Low,df.Close)
    df['CDLRISEFALL3METHODS']=talib.CDLRISEFALL3METHODS(df.Open,df.High,df.Low,df.Close)
    df['CDLSEPARATINGLINES']=talib.CDLSEPARATINGLINES(df.Open,df.High,df.Low,df.Close)
    df['CDLSHOOTINGSTAR']=talib.CDLSHOOTINGSTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLSHORTLINE']=talib.CDLSHORTLINE(df.Open,df.High,df.Low,df.Close)
    df['CDLSPINNINGTOP']=talib.CDLSPINNINGTOP(df.Open,df.High,df.Low,df.Close)
    df['CDLSTALLEDPATTERN']=talib.CDLSTALLEDPATTERN(df.Open,df.High,df.Low,df.Close)
    df['CDLSTICKSANDWICH']=talib.CDLSTICKSANDWICH(df.Open,df.High,df.Low,df.Close)
    df['CDLTAKURI']=talib.CDLTAKURI(df.Open,df.High,df.Low,df.Close)
    df['CDLTASUKIGAP']=talib.CDLTASUKIGAP(df.Open,df.High,df.Low,df.Close)
    df['CDLTHRUSTING']=talib.CDLTHRUSTING(df.Open,df.High,df.Low,df.Close)
    df['CDLTRISTAR']=talib.CDLTRISTAR(df.Open,df.High,df.Low,df.Close)
    df['CDLUNIQUE3RIVER']=talib.CDLUNIQUE3RIVER(df.Open,df.High,df.Low,df.Close)
    df['CDLUPSIDEGAP2CROWS']=talib.CDLUPSIDEGAP2CROWS(df.Open,df.High,df.Low,df.Close)
    df['CDLXSIDEGAP3METHODS']=talib.CDLXSIDEGAP3METHODS(df.Open,df.High,df.Low,df.Close)
    return df

#     def lag(n):
#         df.loc[df.Close.shift(-n)>df.Close,'y']=1
#         df.loc[df.Close.shift(-n)<df.Close,'y']=-1
#         df.loc[df.Close.shift(-n)==df.Close,'y']=0

UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
print(datetime.utcnow()+timedelta(hours=7))


def main_run(pair="EURUSD",timeframe=MT5_TIMEFRAME_M1, point=5000): 
    
    # dfm1=getMT5data("EURUSD",MT5_TIMEFRAME_M1,10000)
    # dfm2=getMT5data("EURUSD",MT5_TIMEFRAME_M2,10000)
    # dfm5=getMT5data("EURUSD",MT5_TIMEFRAME_M5,10000)
    # dfm15=getMT5data("EURUSD",MT5_TIMEFRAME_M15,10000)
    # dfm30=getMT5data("EURUSD",MT5_TIMEFRAME_M30,10000)
    dfh1=getMT5data(pair,timeframe,point)
    # dfh4=getMT5data("EURUSD",MT5_TIMEFRAME_H4,10000)
    # dfh12=getMT5data("EURUSD",MT5_TIMEFRAME_H12,10000)
    # df=pd.concat([dfm1,dfm2,dfm5,dfm15,dfm30,dfh1,dfh4,dfh12])
    df=copy.copy(dfh1)
    df=df.reset_index(drop=True)
    print ("data count:" ,len(df))

    def lag(df,n):
        df.loc[df.Close.shift(-n)>df.Close,'lag_'+str(n)]=1
        df.loc[df.Close.shift(-n)<df.Close,'lag_'+str(n)]=-1
        df.loc[df.Close.shift(-n)==df.Close,'lag_'+str(n)]=0
        return df

    for i in range(10): # run from lag 1 to lag 10
        lag(df,i+1)

    # df.dropna(inplace=True)



    df.index=df.Date

    df.drop(columns=['Open', 'High', 'Low', 'Date'], axis=1, inplace=True)

    #macd
    # df['30 mavg'] =pd.Series.rolling(df['Close'], window=30).mean()
    df['200_mavg'] =pd.Series.rolling(df['Close'], window=200).mean()
    df['26_ema'] = pd.Series.ewm(df['Close'], span=26).mean()
    df['12_ema']=pd.Series.ewm(df['Close'], span=12).mean()
    df['MACD'] = (df['12_ema'] - df['26_ema'])
    df['Signal'] = pd.Series.ewm(df['MACD'], span=9).mean()
    df['Crossover'] = df['MACD'] - df['Signal']
    value=df['Crossover'][-1:].mean()
    previousvalue=df['Crossover'][-2:].head(1).mean()

    def majortrend(row):
        avg200=row['200_mavg']
        curentvalue=row['Close']
        majortrend =""

        if (avg200 <curentvalue):

            majortrend="1"
        elif (avg200 >curentvalue):
            majortrend ="-1"
        else:
            majortrend= "0"
    #     print('major ', majortrend,pair,avg200 ,curentvalue)    
        return majortrend

    df['majortrend']=df.apply(majortrend,axis=1)


    return df



df=main_run("XAUUSD",MT5_TIMEFRAME_H1,500)
df
