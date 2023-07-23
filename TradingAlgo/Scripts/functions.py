import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import xlsxwriter
from datetime import datetime, date, timedelta
import yfinance as yf
import seaborn as sns
import requests


def movingAverageCrossover(stock, shortWindow, longWindow):
    prices = pd.DataFrame()
    prices["ShortEMA"] = stock.ewm(span = shortWindow, adjust = False).mean()
    prices["LongEMA"] = stock.ewm(span = longWindow, min_periods=shortWindow, adjust = False).mean()
    prices.dropna()
    prices["Signal"] = np.where(prices["ShortEMA"] > prices["LongEMA"], 1, 0)
    #print(prices["Signal"].iloc[-1])
    if (prices["Signal"].iloc[-1] == 1):
        return 1
    elif (prices["Signal"].iloc[-1] == 0):
        return 0


def movingAverageCheck(stock, shortWindow):
    prices = pd.DataFrame()
    prices["ShortEMA"] = stock.ewm(span = shortWindow, adjust = False).mean()
    prices.dropna()
    #print(prices["Signal"].iloc[-1])
    if (prices["ShortEMA"].iloc[-1] > stock.iloc[-1]):
        return 1
    else:
        return 0
def get_EMA(stock, start, end, window):
    prices = yf.download(stock, start=start, end=end)
    prices.dropna()
    prices["EMA"] = prices["Close"].rolling(window).mean()
    return prices["EMA"]

def movingAverageCrossoverBacktest(stock, start, end, shortWindow, longWindow):
    prices = yf.download(stock, start=start, end=end)
    prices.dropna()
    prices["ShortEMA"] = prices["Close"].ewm(span = shortWindow).mean()
    prices["LongEMA"] = prices["Close"].ewm(span = longWindow, min_periods=shortWindow).mean()
    prices.dropna()
    prices["Signal"] = np.where(prices["ShortEMA"] > prices["LongEMA"], 1, 0)
    total = 0
    buy = 0
    sell = 0
    for i in range(len(prices)):
        

        if (prices["Signal"][i-1] == 0) & (prices["Signal"][i] == 1):
            buy = float(prices["Close"][i])

        elif (prices["Signal"][i-1] == 1) & (prices["Signal"][i] == 0):
            sell = float(prices["Close"][i])
            #print("Buy" + str(buy))
            #print(sell)
            total += (sell - buy)
            buy = 0
            sell = 0

    print(total)

def get_rsi(close, lookback):
    ret = close.diff()
    up = []
    down = []
    for i in range(0, len(ret)):
        if (ret[i] < 0):
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up = pd.Series(up)
    down = pd.Series(down).abs()
    up_ewm = up.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm / down_ewm
    rsi = 100 - (100/(1+rs))
    rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(close.index)
    #print(rsi_df.to_string())
    rsi_df.dropna()   
    if (rsi_df["rsi"].values[-1:] >= 80):
        return 0
    elif (rsi_df["rsi"].values[-1:] <= 20):
        return 1

def get_sp_500_data(f, sp_500_list, sp_500_df, stocks_owned):
    for i in range(0, len(sp_500_list)):
            #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 6, 10))
        if ((get_rsi(sp_500_df[f"{sp_500_list[i]}"], 7) == 1) and movingAverageCrossover2(sp_500_df[f"{sp_500_list[i]}"], 30, 120) == 1) and (movingAverageCrossover2(sp_500_df[sp_500_list[i]], 10, 30) == 1): 
            if sp_500_list[i] in stocks_owned:
                pass
            else:
                f.write(f"Buy {sp_500_list[i]} \n")
                stocks_owned.append(sp_500_list[i])
        elif ((get_rsi(sp_500_df[f"{sp_500_list[i]}"], 7) == 0) or (movingAverageCrossover2(sp_500_df[f"{sp_500_list[i]}"], 30, 120) == 0)) and (sp_500_list[i] in stocks_owned): 
            if sp_500_list[i] in stocks_owned:
                f.write(f"Sell {sp_500_list[i]} \n")
                stocks_owned.remove(sp_500_list[i])
    return (stocks_owned)
        
                #print(functions.get_rsi(sp_500_df[f"{sp_500_list[i]}"], 14))
                #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 8, 14))
                #print(" ")
                #     test_start += delta
def get_nas_100(f, nas_list, nas_df, stocks_owned):
    for i in range(0, len(nas_list)):
            #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 6, 10))
        if ((get_rsi(nas_df[f"{nas_list[i]}"], 14) == 1) and movingAverageCrossover2(nas_df[f"{nas_list[i]}"], 20, 50) == 1):
            f.write(f"Buy {nas_list[i]} \n")
        elif (((get_rsi(nas_df[f"{nas_list[i]}"], 14) == 0) or movingAverageCrossover2(nas_df[f"{nas_list[i]}"], 20, 50) == 0) & (nas_list[i] in stocks_owned)):
            f.write(f"Sell {nas_list[i]} \n")
            
                #print(functions.get_rsi(sp_500_df[f"{sp_500_list[i]}"], 14))
                #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 8, 14))
                #print(" ")
                #     test_start += delta
#def check_overlap(stock_close):

def get_sp_500_data_test(f, sp_500_list, sp_500_df):
        for i in range(0, len(sp_500_list)):
            #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 6, 10))
            if ((get_rsi(sp_500_df[f"{sp_500_list[i]}"], 14) == 1) and movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 5, 20) == 1):
                print("Yes")
            elif ((get_rsi(sp_500_df[f"{sp_500_list[i]}"], 14) == 0) or movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 5, 20) == 0):
                #f.write(f"Sell {sp_500_list[i]} \n")
                pass
                #print(functions.get_rsi(sp_500_df[f"{sp_500_list[i]}"], 14))
                #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 8, 14))
                #print(" ")
                #     test_start += delta

def print_rsi(close, lookback):
    ret = close.diff()
    up = []
    down = []
    for i in range(0, len(ret)):
        if (ret[i] < 0):
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up = pd.Series(up)
    down = pd.Series(down).abs()
    up_ewm = up.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm / down_ewm
    rsi = 100 - (100/(1+rs))
    rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(close.index)
    #print(rsi_df.to_string())
    rsi_df.dropna() 
    return rsi_df
def movingAverageCrossover2(stock, shortWindow, longWindow):
    prices = pd.DataFrame()
    prices["ShortEMA"] = stock.rolling(shortWindow).mean()
    prices["LongEMA"] = stock.rolling(window = longWindow, min_periods=shortWindow).mean()
    prices.dropna()
    #print(prices[prices["ShortEMA"] > prices["LongEMA"]])
    if (prices["ShortEMA"][-1] > prices["LongEMA"][-1]):
        return 1
    elif (prices["LongEMA"][-1] > prices["ShortEMA"][-1]):
        return 0

'''
def get_sp_500_data_test(f, sp_500_list, sp_500_test, sp_500_df, stocks_owned):
    for i in range(0, len(sp_500_list)):
            #print(functions.movingAverageCrossover(sp_500_df[f"{sp_500_list[i]}"], 6, 10))
        if ((get_rsi(sp_500_test[f"{sp_500_list[i]}"]["Close"], 14) == 1) and movingAverageCrossover2(sp_500_test[f"{sp_500_list[i]}"], 20, 50) == 1):
                pass
            else:
                f.write(f"Buy {sp_500_list[i]} \n")
        elif (((get_rsi(sp_500_df[f"{sp_500_list[i]}"], 14) == 0) or movingAverageCrossover2(sp_500_df[f"{sp_500_list[i]}"], 20, 50) == 0) & (sp_500_list[i] in stocks_owned)):
            if sp_500_list[i] in stocks_owned:
                f.write(f"Sell {sp_500_list[i]} \n")
        
        '''