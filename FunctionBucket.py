from SizeBMRIIG_Brakedown import ccm_june1
import pandas as pd
import numpy as np
from pandas.tseries.offsets import *
########################################################################################################################
# Size
def sz_bucket(row):
    if row['me'] == np.nan:
        value = ''
    elif row['me'] <= row['sizemedian']:
        value = 'S'
    else:
        value = 'B'
    return value

# Book-to-Market
def bm_bucket(row):
    if 0 <= row['beme'] <= row['bm30']:
        value = 'L'
    elif row['beme'] <= row['bm70']:
        value = 'M'
    elif row['beme'] > row['bm70']:
        value = 'H'
    else:
        value = ''
    return value

# Robustness Indicator
def  ri_bucket(row):
    if 0<= row['ri'] <= row['ri30']:
        value = 'W'
    elif row['ri'] <= row['ri70']:
        value = 'N'
    elif row['ri'] > row['ri70']:
        value = 'R'
    else:
        value = ''
    return value

# Investment Growth (used as proxy for conservativeness) indicator

def ig_bucket(row):
    if 0 <= row['ig'] <= row['ig30']:
        value = 'C'
    elif row['ig'] <= row['ig70']:
        value = 'N'
    elif row['ig'] > row['ig70']:
        value = 'A'
    else:
        value = ''
    return value
########################################################################################################################
