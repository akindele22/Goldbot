from msilib import datasizemask
from turtle import xcor
#from mirror import *
import pandas as pd 
import numpy as np 
import MetaTrader5 as mt 
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import pickle
import time
import os
import talib


##################################################  Logics involved    ###################################################################


# data1 = data.copy()

def TI(df):
#     df['Date'] = pd.to_datetime(df['time'], utc=True, unit='s')
#     df.drop('time', axis=1, inplace=True)
    df['time'] = df.index

    # indicators
    # https://github.com/mrjbq7/ta-lib/blob/master/docs/func.md
    open_price, high, low, close = np.array(df['open']), np.array(df['high']), np.array(df['low']), np.array(df['close'])
    volume = np.array(df['tick_volume'])
    # cycle indicators
    #df.loc[:, 'HT_DCPERIOD'] = talib.HT_DCPERIOD(close)
#     print(df.loc[:, 'HT_DCPERIOD'] )
    # momemtum indicators
    df.loc[:, 'BOP'] = talib.BOP(open_price, high, low, close)
    df.loc[:, 'TRIX'] = talib.TRIX(close, timeperiod=30)
    # pattern recoginition
    df.loc[:, 'CDL2CROWS'] = talib.CDL2CROWS(open_price, high, low, close)
    df.loc[:, 'CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(open_price, high, low, close)
    df.loc[:, 'CDL3INSIDE'] = talib.CDL3INSIDE(open_price, high, low, close)
    df.loc[:, 'CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(open_price, high, low, close)
    # volatility indicators
    df.loc[:, 'ATR'] = talib.ATR(high, low, close, timeperiod=7)
    df.loc[:, 'NATR'] = talib.NATR(high, low, close, timeperiod=20)
    df.loc[:, 'TRANGE'] = talib.TRANGE(high, low, close)
    # volume indicators
    #df.loc[:, 'AD'] = talib.AD(high, low, close, volume)
    #df.loc[:, 'ADOSC'] = talib.ADOSC(high, low, close, volume, fastperiod=10, slowperiod=20)
    #df.loc[:, 'OBV'] = talib.OBV(close, volume)

    df.fillna(df.mean(), inplace=True)
    df.dropna(inplace=True)
    df.set_index('time', inplace=True)
    return df


cwd = os.getcwd()
mydir = cwd
def pred_clf_xau():
    loaded_model = pickle.load(open("XAUUSDc_model.pkl", "rb"))
    return loaded_model


#send market order
# function to send a market order
def market_order7(symbol, volume, order_type):
    if order_type == 'buy':
        tick = mt.symbol_info_tick(symbol)
        order_dict = {'buy': 0, 'sell': 1}
        price_dict = {'buy': tick.ask, 'sell': tick.bid}
        point = mt.symbol_info(symbol).point
        

        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_dict[order_type],
            "price": price_dict[order_type],
            "sl": price_dict[order_type] - 3000 * point,
            "tp": price_dict[order_type] + 10000* point,
            "magic": 100,
            "comment": "python market order",
            "type_time": mt.ORDER_TIME_GTC,
            
        }

        order_result = mt.order_send(request)
        print(order_result)
        logs = ['Order: ', str(order_result),
                '-------\n' ]
        with open('logsAUDCAD.txt', 'a') as f:
            for log in logs:
                f.write(log)
                f.write('\n')
        f.close()

        return order_result
    if order_type == 'sell':
        tick = mt.symbol_info_tick(symbol)
        order_dict = {'buy': 0, 'sell': 1}
        price_dict = {'buy': tick.ask, 'sell': tick.bid}
        point = mt.symbol_info(symbol).point
        

        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_dict[order_type],
            "price": price_dict[order_type],
            "sl": price_dict[order_type] + 3000 * point,
            "tp": price_dict[order_type] - 10000 * point,
            "magic": 100,
            "comment": "python market order",
            "type_time": mt.ORDER_TIME_GTC,
            
        }

        order_result = mt.order_send(request)
        print(order_result)
        logs = ['Order: ', str(order_result),
                '-------\n' ]
        with open('logsAUDCAD.txt', 'a') as f:
            for log in logs:
                f.write(log)
                f.write('\n')
        f.close()

        return order_result


# function to close an order base don ticket id
def close_order7(ticket):
    positions = mt.positions_get()

    for pos in positions:
        tick = mt.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}

        if pos.ticket == ticket:
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "magic": 100,
                "comment": "python close order",
                "type_time": mt.ORDER_TIME_GTC,
                
            }

            order_result = mt.order_send(request)
            print(order_result)

            return order_result

    return 'Ticket does not exist'


def get_data7(symbol, timeframe,roll_period):
    ohlc_data7 = pd.DataFrame(mt.copy_rates_from_pos(symbol,
                                                timeframe,
                                                1,
                                                roll_period))
    #fig = px.line(ohlc_data7, x=ohlc_data7['time'], y=ohlc_data7['close'])
    ohlc_data7['time']=pd.to_datetime(ohlc_data7['time'], unit='s')
    ohlc_data7.to_csv('ohlc_data7.csv')
    return ohlc_data7
#def get_data72(symbol, timeframe,roll_period):
    #ohlc_data72 = pd.DataFrame(mt.copy_rates_from_pos(symbol,
                                                #timeframe,
                                                #1,
                                                #roll_period))
    #fig = px.line(ohlc_data7, x=ohlc_data7['time'], y=ohlc_data7['close'])
    #ohlc_data72['time']=pd.to_datetime(ohlc_data72['time'], unit='s')
    #ohlc_data72.to_csv('ohlc_data72.csv')
    #return ohlc_data72

def get_exposure7(symbol):
    positions = mt.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure



print('code complete')
###################################################### Beginning of code (runtime)###########################################################
def trade91(): 
    symbol = 'AUDCADm'
    timeframe = mt.TIMEFRAME_H2
    VOLUME = 0.01
    roll_period = 100
    
    mt.initialize()

    while True:
        cwd = os.getcwd()
        mydir = cwd
        for f in os.listdir(mydir):
            if not f.endswith("7.csv"):
                continue
            os.remove(os.path.join(mydir, f))


        exposure = get_exposure7(symbol)
        # 30mins data
        get_data7(symbol, timeframe,roll_period)
        ohlc_data7 = pd.read_csv('ohlc_data7.csv')
        data7 = ohlc_data7.copy()
        #data7 = data7.reset_index('date')
        print('code complete')
        df = TI(data7)


        X = df
        y = df
        X_train, X_test, y_train, y_test2 = train_test_split(X,y,test_size=0.2, random_state=42)
        
        
        direction = 'flat'
        if (pred_clf_xau().predict(X_test) == 1).any():
            direction = 'buy'
        elif (pred_clf_xau().predict(X_test) == -1).any():
            direction = 'sell'
        else:
            direction = 'pass'

        
        # trading logic
        if direction == 'buy':
            # if we have a BUY signal, close all short positions
            #for pos in mt.positions_get():
                #if pos.type == 1:  # pos.type == 1 represent a sell order
                    #close_order7(pos.ticket)

            # if there are no open positions, open a new long position
            #if not mt.positions_total():
            market_order7(symbol, VOLUME, direction)

        elif direction == 'sell':
            # if we have a SELL signal, close all short positions
            #for pos in mt.positions_get():
                #if pos.type == 0:  # pos.type == 0 represent a buy order
                    #close_order7(pos.ticket)

            # if there are no open positions, open a new short position
            #if not mt.positions_total():
            market_order7(symbol, VOLUME, direction)

        
        
        elif direction == 'sell':
            pass

        current_time = datetime.now()
        str_current_time = str(current_time)
        logs = ['time: ', str_current_time,
                '-------\n' 
                'symbol: ', str(symbol),
                '-------\n'
                'exposure: ', str(exposure),
                '-------\n'
                'signal: ', str(direction),
                '-------\n',
                '-------\n']
        with open('logsAUDCAD.txt', 'a') as f:
            for log in logs:
                f.write(log)
                f.write('\n')
        f.close()
        print('time: ', datetime.now())
        print('symbol: ', symbol)
        print('exposure: ', exposure)
        print('signal: ', direction)
        print('-------\n')


        cwd = os.getcwd()
        mydir = cwd
        for f in os.listdir(mydir):
            if not f.endswith("7.csv"):
                continue
            os.remove(os.path.join(mydir, f))
        time.sleep(600)

    #fig.show()
    #ohlc_data7
    

####################################################### 