import numpy as np
import pandas as pd


data = pd.read_csv('cstmc-CSV-en.csv', sep='|', error_bad_lines=False)
output = data.groupby('BeginDate')['material'].value_counts()
print(output)
output.to_csv('material-stats.csv')
