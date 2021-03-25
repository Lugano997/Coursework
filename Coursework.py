# Name: Dario Miranda


# Importing the relevant packages

import pandas as pd
import numpy as np
# import datetime as dt
# import psycopg2
# import matplotlib.pyplot as plt
# from dateutil.relativedelta import *
# from pandas.tseries.offsets import *
# from scipy import stats

# Importing and visualizing the datasets

comp = pd.read_csv('CRSP_Compustat.csv')

# Convert the datadate into Dates

comp['datadate'] = comp['datadate'].astype(str)
comp['datadate'] = pd.to_datetime(comp['datadate'])

# Creating a year column
comp['year'] = comp['datadate'].dt.year

# Generating the Preferred Stocks column
comp['ps'] = np.where(comp['pstkrv'].isnull(), comp['pstkl'], comp['pstkrv'])
comp['ps'] = np.where(comp['ps'].isnull(), comp['pstk'], comp['ps'])
comp['ps'] = np.where(comp['ps'].isnull(), 0, comp['ps'])

# Book Equity creation
# Firstly, we have to clean our dataset.

# Replacing all the missing values in TXDITC with 0.

comp['txditc'] = comp['txditc'].fillna(0)

# Creating the BE column, excluding negative values.

comp['be'] = comp['seq'] + comp['txditc'] - comp['ps']
comp['be'] = np.where(comp['be']>0, comp['be'],np.nan)

# We are going to create two other relevant variables in order to compute RMW and CMA factors.
# In particular, we are going to create a column containing indicators for robustness of profitability on the following
# formula. Robust Indicator : ri = (Revenue - COGS - SGA)/BE. Subsequently, we are going to use these indicators
# to create portfolios baskets divided in Robust, Neutral and Weak.

# Cleaning the data

comp['revt'] = comp['revt'].fillna(0)
comp['cogs'] = comp['cogs'].fillna(0)
comp['xsga'] = comp['xsga'].fillna(0)

# We have to divide for the BE value, so in order to avoid a divided for 0 error we are going to remove all the nan

comp['be'] = pd.to_numeric(comp['be'], errors='coerce')
comp = comp[comp['be'].notnull()]

# Creating the RI column
comp['ig'] = comp['at'].pct_change()
comp['count'] = comp.groupby(['GVKEY']).cumcount()
comp['ig'] = np.where(comp['count'] == 0, np.nan, comp['ig'])

comp['ri'] = (comp['revt']-comp['cogs']-comp['xsga'])/comp['be']

# Now to create and indicator for CMA we have decided to use the cumulative percentage growth in total asset as proxy
# for the investment level for the firms. Once that we have created our series we will divide the firms in baskets
# based on the investments growth. Our indicator will be created as follow:
# Investment Growth: IG = (Total asset(t) - Total asset(t-1))/Total asset(t-1)
# Unfortunately, as a consquences of the applied formula we are going to lose an observation.

comp = comp.sort_values(by=['LPERMNO', 'datadate'])
comp['count'] = comp.groupby(['LPERMNO']).cumcount()  # Note that this starts from zero
# lo usiamo per evitare l'effetto sopravvivenza

# Some companies change fiscal year end in the middle of the calendar year
# In these cases, there are more than one annual record for accounting data
# We need to select the last annual record in a given calendar year
comp = comp.sort_values(by=['LPERMNO', 'year', 'datadate'])
comp = comp.drop_duplicates(subset=['LPERMNO', 'year'], keep='last')

# keep necessary variables and rename for future matching
comp = comp[['LPERMNO', 'GVKEY', 'datadate', 'year', 'be', 'count','ri', 'ig']].rename(columns={'LPERMNO': 'PERMNO'})

