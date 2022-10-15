from msilib import datasizemask
from turtle import xcor
import pandas as pd 
import numpy as np 
import MetaTrader5 as mt 
from datetime import datetime
import pickle
import time
import os
from XAUUSD import trade7
from BTCUSD import trade8
#from USDCHF import trade9
#from AUDCAD import trade91

from multiprocessing import Process

if __name__ == '__main__':
    print('initializing......')
    print('initializing......')
    print('initializing......')
    print('picking trades.................................................................................................................')
    p7 = Process(target=trade7)
    p7.start()
    p8 = Process(target=trade8)
    p8.start()
    #p9 = Process(target=trade9)
    #p9.start()
    #p91 = Process(target=trade91)
    #p91.start()
    p7.join()
    p8.join()
    #p9.join()
    #p91.join()



