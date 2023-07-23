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
start = datetime(2023,3,21)
end = datetime.now()
test_start = datetime(2023,1,1)
import backtrader as bt

stocks_owned = ['MUC', 'BOX', 'MBAC', 'SRL', 'SU', 'BP', 'UAL', 'LVS', 'MOS', 'BBVA', 'SHEL', 'ETN', 'HWM', 'IR', 'INSW', 'TNP', 'GJO', 'SLQT', 'WHG']

check = yf.download(stocks_owned, start=start)["Close"]

print(check)