import pandas as pd
import numpy as np
import tabulate as tb

dtata = pd.DataFrame({'COL1': [1, 1, 1, 5, 5, 7], 'COL2': [2, 2, 3, 10, 10, 0.08], 'COL3': [1, 1, 1, 1, 1, 1]})

print(dtata)

cici = dtata.groupby(['COL1', 'COL2']).sum().reset_index()

print(cici)
