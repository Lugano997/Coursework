import pandas as pd
import numpy as np
from Coursework import comp
from MarketData import crspjune
from pandas.tseries.offsets import *
from Merge_CRSP_Compustat import ccm_june

# Now we can create a new dataset containing the Size, BM, RI and IG breakdown in order to prepare the data for
# the factors construction.

# We are going to consider only the stocks with the following characteristics:
# Traded on the Ney York Stocks Exchange (EXCHCD = 1);
# Positive Book to Market;
# Positive Market Capitalization;
# Registered in the dataset for at least 2 year in order to avoid the "Survival Effect".

nyse_s = ccm_june[(ccm_june['EXCHCD']==1) & (ccm_june['beme']>0) & (ccm_june['me']>0) & (ccm_june['count']>1)]

# We have now to breakdown all the factors to then create our portfolios baskets.

# SIZE
nyse_size = nyse_s.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedian'})

# BEME
nyse_beme = nyse_s.groupby(['jdate'])['beme'].describe(percentiles=[0.3,0.7]).reset_index()
nyse_beme = nyse_beme[['jdate','30%','70%']].rename(columns={'30%':'bm30','70%':'bm70'})

# Robustness indicator breakdown
nyse_ri = nyse_s.groupby(['jdate'])['ri'].describe(percentiles=[0.3,0.7]).reset_index()
nyse_ri = nyse_ri[['jdate','30%','70%']].rename(columns={'30%':'ri30', '70%':'ri70'})

# Investment growth indicator breakdown
nyse_ig = nyse_s.groupby(['jdate'])['ig'].describe(percentiles=[0.3,0.7]).reset_index()
nyse_ig = nyse_ig[['jdate','30%','70%']].rename(columns={'30%':'ig30', '70%':'ig70'}).reset_index()

# Now we have to aggregate the last four datasets.
nyse_agg1 = pd.merge(nyse_size,nyse_beme, how='inner', on=['jdate'])
nyse_agg2 = pd.merge(nyse_ri, nyse_ig, how='inner', on=['jdate'])
nyse_aggtot = pd.merge(nyse_agg1,nyse_agg2, how='inner', on=['jdate'])

# Removing the index column from nyse_aggtot
nyse_aggtot = nyse_aggtot.drop(['index'], axis=1)

ccm_june1 = pd.merge(ccm_june, nyse_aggtot, how='left', on=['jdate'])

# Now we can define some functions to create the portfolios baskets and finally get the returns to compute the factors.

########################################################################################################################
