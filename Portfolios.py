from SizeBMRIIG_Brakedown import ccm_june1
import pandas as pd
import numpy as np
from FunctionBucket import *
from pandas.tseries.offsets import *
from MarketData import crsp2


# Now we can construct the portfolios based on the indicators values.

# Creating the Size Portfolio.
ccm_june1['szport'] = np.where((ccm_june1['beme'] > 0) & (ccm_june1['me'] > 0) & (ccm_june1['count'] >= 1),
                               ccm_june1.apply(sz_bucket, axis=1), '')

# Creating the Book-To-Market Portfolio.
ccm_june1['bmport'] = np.where((ccm_june1['beme'] > 0) & (ccm_june1['me'] > 0) & (ccm_june1['count'] >= 1),
                               ccm_june1.apply(bm_bucket, axis=1), '')

# Creating the Robustness portfolio.
ccm_june1['riport'] = np.where((ccm_june1['beme'] > 0) & (ccm_june1['me'] > 0) & (ccm_june1['count'] >= 1),
                               ccm_june1.apply(ri_bucket, axis=1), '')

# Creating the Conservativeness portfolio
ccm_june1['igport'] = np.where((ccm_june1['beme'] > 0) & (ccm_june1['me'] > 0) & (ccm_june1['count'] >= 1),
                               ccm_june1.apply(ig_bucket, axis=1), '')


# We are going to keep only the positive Book-to-Market value. Due to this reason we have to create a new column that
# will indicate which stocks present this feature.
ccm_june1['posbm'] = np.where((ccm_june1['beme'] > 0) & (ccm_june1['me'] > 0) & (ccm_june1['count'] >= 1), 1, 0)

# Highliting the missing value.
ccm_june1['nonmissport'] = np.where((ccm_june1['bmport'] != ''), 1, 0)

# Keeping only the relevant variables, and generating the Fama-French years column into a new dataset.
june = ccm_june1[['PERMNO', 'jdate', 'bmport', 'szport', 'riport', 'igport','posbm', 'nonmissport']]
june['ffyear'] = june['jdate'].dt.year

# Keeping only the useful variables from crsp_s2 and merging it with the relevant variables of june dataset.
crsp_s4 = crsp2[['date', 'PERMNO', 'RET_ADJ', 'me', 'lme', 'ffyear', 'jdate']]
ccm = pd.merge(crsp_s4,
               june[['PERMNO', 'ffyear', 'szport', 'bmport','riport', 'igport', 'posbm', 'nonmissport']], how='left',
               on=['PERMNO', 'ffyear'])
########################################################################################################################
