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

ap = yf.download(["AAPL"], start=datetime(2022,1,1))["Close"]


print(functions.print_rsi(ap, 5 ))
functions.movingAverageCrossover2(ap, 5, 9)