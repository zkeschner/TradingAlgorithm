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
stocks_owned = ['MKTX', 'BP', 'LVS', 'BBVA', 'SHEL', 'HWM', 'IR', 'GJO', 'SLQT', 'MTAL', 'ZGN', 'ATVI', 'ABBV', 'IPG']
sp_500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
start = datetime(2022,1,1)
sp_500_list = pd.read_html(sp_500_url)
payload=pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
nas_list = payload[4]["Ticker"]
nas_list = list(nas_list)
sp_500_list = (sp_500_list[0]["Symbol"])
sp_500_list = list(sp_500_list)
sp_500_list.remove("BF.B")
sp_500_list.remove("BRK.B")
nas_df = yf.download(nas_list, start=start)["Close"]
file = open("NYSE.txt", "r")
data = file.read()
f = open("stockinfo.txt", "w")  
tickers_list = data.split("\n")
sp_500_df = yf.download(sp_500_list, start=start)["Close"]
stocks_owned = functions.get_sp_500_data(f, nas_list, nas_df, stocks_owned)
stocks_owned = functions.get_sp_500_data(f, sp_500_list, sp_500_df, stocks_owned)
#print(tickers_list)
Nyse_df = yf.download(tickers_list, start = datetime(2022,1,1))["Close"]
stocks_owned = functions.get_sp_500_data(f, tickers_list, Nyse_df,stocks_owned)

print(stocks_owned)