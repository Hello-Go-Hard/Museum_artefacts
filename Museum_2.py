import numpy as np
import pandas as pd


data = pd.read_csv('cstmc-CSV-en.csv', sep='|', error_bad_lines=False)
ctgr = []
ctgr.append(data['category1'].value_counts())
ctgr.append(data['category2'].value_counts())
ctgr.append(data['category3'].value_counts())
categories = data['category1'].unique()
categories_dict = {}
for i in categories:
    categories_dict[i] = 0
for i in ctgr:
    for j in categories:
        try:
            categories_dict[j] += i[j]
        except KeyError:
            continue
        except TypeError:
            continue
print(categories_dict)
keys = []
values = []
for i, j in categories_dict.items():
    keys.append(i)
    values.append(j)
categories_dict = {'category': keys, 'count': values}
output = pd.DataFrame(categories_dict)
output.to_csv('object-stats.csv')
