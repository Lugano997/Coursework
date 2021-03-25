import pandas as pd
import numpy as np
from Coursework import comp
from MarketData import crspjune
from pandas.tseries.offsets import *
import MarketData
import Coursework

# Part 3 Merge CRSP with Compustat data on June of each year (Hard to understand but very important)

# Match fiscal year ending calendar year t (compustat) with June t+1 (crsp)
# --> All portfolios are formed on June t+1
# Why? --> Fama argues that it may take at least 6 months for accounting information to be incorporated into stock
# price or return
# For example, the datadate of accounting information for firm A is 20180930, we should start to use on 20190631
# In a nutshell, we should convert the datadate to the end of the year and then add 6 month
# e.g, 20180930 --> 20181231 --> 20190630)
#################################################################################################################

# Prepare compustat data for matching
comp['jdate'] = comp['datadate'] + YearEnd(0)
comp['jdate'] = comp['jdate'] + MonthEnd(6)

# keep necessary variables in Compustat
comp2 = comp[['PERMNO', 'jdate', 'be', 'ri', 'ig', 'count']]

# keep necessary variables in crspjune
crspjune2 = crspjune[['PERMNO', 'PERMCO', 'jdate', 'RET_ADJ', 'me', 'lme', 'dec_me', 'EXCHCD']]

# Merge the crspjune2 and compustat2
ccm_june = pd.merge(crspjune, comp2, how='inner', on=['PERMNO', 'jdate'])

# Generate book to market ratio (B/M)
ccm_june['beme'] = ccm_june['be'] / ccm_june['dec_me']
