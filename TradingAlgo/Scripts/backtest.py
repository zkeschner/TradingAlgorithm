import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import xlsxwriter
from datetime import datetime, date, timedelta
import yfinance as yf
import seaborn as sns
import functions 
import requests
sp_500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp_500_list = pd.read_html(sp_500_url)
payload=pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
nas_list = payload[4]["Ticker"]
nas_list = list(nas_list)
sp_500_list = (sp_500_list[0]["Symbol"])
sp_500_list = list(sp_500_list)
sp_500_list.remove("BF.B")
sp_500_list.remove("BRK.B")
file = open("NYSE.txt", "r")
data4 = file.read()
tickers_list = data4.split("\n")


start = datetime(2018,1,1)
sp_500_df = pd.read_csv('Sp_500.csv')
Nyse_df = pd.read_csv('NYSE.csv')
nas_df = pd.read_csv('NAS.csv')
stocks_owned = []
#nested for loop? One for days, one to run through the lists
total = 0
Nyse_test_df = Nyse_df
for i in range(0, len(tickers_list)):

    print(i)
    #add new column to the databases called signal for buy and sell signals  (If want to improve can use open and close in future)
    #use floor division of 1000 by close price to see how many shares were bought 
    buy = 0
    sell = 0
    amount = 0
    for j in range(3, len(Nyse_df)):
        if (functions.movingAverageCrossover(Nyse_test_df[tickers_list[i]].iloc[0:j], 30, 120) == 1) and (buy == 0): #functions.get_rsi(Nyse_test_df[f"{tickers_list[i]}"].iloc[0:j], 14) == 1) and 
            buy = float(Nyse_df[tickers_list[i]].iloc[j])
            amount = 1000 // buy
            #print(buy)
        elif (functions.movingAverageCrossover(Nyse_test_df[tickers_list[i]].iloc[0:j], 30, 120) == 0) and (buy != 0):#((functions.get_rsi(Nyse_test_df[tickers_list[i]].iloc[0:j], 14) == 0) or 
            sell = float(Nyse_df[tickers_list[i]].iloc[j])
            #print(sell)
            total += float((sell - buy) * amount)
            sell = 0
            buy = 0
            amount = 0
        else:
            pass
    sell = 0
    buy = 0
    amount = 0
    print(total)



#nas_test_df = nas_df.iloc[0:i]
#sp_500_test_df = sp_500_df.iloc[0:i]