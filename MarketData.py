# import packages
import pandas as pd
import numpy as np
# import datetime as dt
# import psycopg2
import matplotlib.pyplot as plt
# from dateutil.relativedelta import *
from pandas.tseries.offsets import *
# from scipy import stats
from Coursework import comp

crsp_m = pd.read_csv('CRSP_Stocks.csv')

# Filter data

# The stock exchanges are NYSE(exchange code=1), AMEX(2) and NASDAQ(3)
crsp_m = crsp_m[crsp_m['EXCHCD'].isin([1, 2, 3])]

# Only keep common shares --> share code=10 and 11
crsp_m = crsp_m[crsp_m['SHRCD'].isin([10, 11])]

# Drop missing returns

# Remove string value from numerical return column (e.g., B and C) --> They represent errors
crsp_m['RET'] = pd.to_numeric(crsp_m['RET'], errors='coerce')  # Covert string value to missing value
crsp_m = crsp_m[crsp_m['RET'].notnull()]

# Change variable format to int
crsp_m[['PERMNO', 'PERMCO', 'SHRCD', 'EXCHCD']] = crsp_m[['PERMNO', 'PERMCO', 'SHRCD', 'EXCHCD']].astype(int)

# Covert the data to pandas date format and line up the date to the end of month
crsp_m['date'] = crsp_m['date'].astype(str)
crsp_m['date'] = pd.to_datetime(crsp_m['date'])
crsp_m['jdate'] = crsp_m['date'] + MonthEnd(0)

# Generate adjusted return by considering the delisting return
crsp_m['DLRET'] = pd.to_numeric(crsp_m['DLRET'], errors='coerce')  # Covert string value to missing value
crsp_m['DLRET'] = crsp_m['DLRET'].fillna(0)
crsp_m['RET_ADJ'] = (1 + crsp_m['RET']) * (1 + crsp_m['DLRET']) - 1

# Generate market value (in millions)
crsp_m['me'] = crsp_m['PRC'].abs() * crsp_m['SHROUT'] / 1000  # Price can be negative if is the average of bid and ask


# Sort values and keep necessary variables
crsp_m = crsp_m.sort_values(by=['PERMCO', 'jdate'])
crsp = crsp_m.drop(['DLRET', 'PRC', 'SHROUT', 'RET', 'SHRCD'], axis=1)  # axis=1 refers to column

# Aggregate market cap at firm level --> One firm may have multiple classes of stocks (multiple permnos). In this case,
# we need to aggregate the market cap of all stocks belonging to the firm
# The aggregated market cap will be assigned to the permno with the largest market cap

# Permco: 123 --> Stock Class A: Permno: 10001 2 million / Stock Class B: Permno: 10002 1 million

# Permno 10001 : market cap --> 3 million

# Sum of me across different permnos belonging to the same permco in a given date
crsp_summe = crsp.groupby(['jdate', 'PERMCO'])['me'].sum().reset_index()

# Largest market cap within a permco in a given date
crsp_maxme = crsp.groupby(['jdate', 'PERMCO'])['me'].max().reset_index()

# Join by jdate/maxme to find the permno --> find the permno which has the largest market cap under one permco
crsp1 = pd.merge(crsp, crsp_maxme, how='inner', on=['jdate', 'PERMCO', 'me'])

# Drop me column and replace with the sum me
crsp1 = crsp1.drop(['me'], axis=1)

# Join with sum of me to get the correct market cap info
crsp2 = pd.merge(crsp1, crsp_summe, how='inner', on=['jdate', 'PERMCO'])

# Sort by permno and date and also drop duplicates
crsp2 = crsp2.sort_values(by=['PERMNO', 'jdate']).drop_duplicates()


# keep December market cap -> When we calculate value factor (B/M)
# we use the market cap on December in prior year
crsp2['year'] = crsp2['jdate'].dt.year
crsp2['month'] = crsp2['jdate'].dt.month
decme = crsp2[crsp2['month'] == 12]
decme = decme[['PERMNO', 'jdate', 'me']].rename(columns={'me': 'dec_me', 'jdate': 'ffdate'})

# Generate July to June dates --> To make the ffyear is from July of yeat t to June of year t+1
# Our portfolios are rebalanced on each June
# Jan - December (calendar year) --> July - June (ff year) (e.g., 202001 - 202012 --> 201907 - 202006)
crsp2['ffdate'] = crsp2['jdate'] + MonthEnd(-6)
crsp2['ffyear'] = crsp2['ffdate'].dt.year
crsp2['ffmonth'] = crsp2['ffdate'].dt.month

# Generate the market cap of prior month as the portfolio weight (value-weighted portfolio)
crsp2['lme'] = crsp2.groupby(['PERMNO'])['me'].shift(1)  # lagged variable

# Create a dataset in each June (Portfolio forming month) merged with market cap from previous December
# Because there is at least 6 month gap for accounting information to be incorporated into stock price

# Keep only the data on June --> Portfolios are sorted on June of each year
crsp3 = crsp2[crsp2['month'] == 6]

# merge with market cap in last December --> 20190630 <--> 20181231
crspjune = pd.merge(crsp3, decme, how='left', on=['PERMNO', 'ffdate'])

