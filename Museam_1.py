import numpy as np
import pandas as pd


def a():
    data = pd.read_csv('cstmc-CSV-en.csv', sep='|', error_bad_lines=False)
    some_series = data['ManuCountry'].value_counts()
    unknown_countryes = some_series['Unknown']
    print("Unknown  ", unknown_countryes)

    some_series = some_series.drop(labels=['Unknown'])
    print(some_series.idxmax())
    dict = {'country': [some_series.idxmax(), 'Unknown'], 'count': [some_series.max(), unknown_countryes]}
    output = pd.DataFrame(dict)
    output.to_csv('general-stats.csv')


def b():
    data = pd.read_csv('cstmc-CSV-en.csv', sep='|', error_bad_lines=False)
    some_series = data[['ObjectName', 'BeginDate', 'EndDate']]
    duration = []
    some_series_of_nan = data[['BeginDate', 'EndDate']].isna()
    count_of_nan = 0
    for i in some_series_of_nan.index:
        if some_series_of_nan['BeginDate'][i] == False or some_series_of_nan['EndDate'][i] == False:
            count_of_nan += 1
    for i in some_series.index:
        try:
            duration.append(int(some_series['EndDate'][i]) - int(some_series['BeginDate'][i]))
        except ValueError:
            duration.append(0)
    some_series.insert(3, 'new column', duration)
    print(some_series.loc[some_series['new column'].astype(float).idxmax()][['ObjectName', 'new column']])
    print("Unknown  ", count_of_nan)
    dict = {'Object': [some_series.loc[some_series['new column'].astype(float).idxmax()]['ObjectName'], 'NaN date'], 'Duration': [ some_series['new column'].max(), count_of_nan]}
    output = pd.DataFrame(dict)
    output.to_csv('general-stats.csv')


def c():
    data = pd.read_csv('cstmc-CSV-en.csv', sep='|', error_bad_lines=False)
    some_series = data[['ObjectName', 'Weight']]
    count_of_nan = 0
    for i in some_series.index:
        little_string = str(some_series['Weight'][i])
        increment = 0
        while little_string[increment].isnumeric() or little_string[increment] == '.':
            increment += 1
        little_string = little_string[:increment]
        if little_string != '':
            some_series['Weight'][i] = float(little_string)
        else:
            count_of_nan += 1
            some_series['Weight'][i] = 1000.0
    print(some_series)
    print(some_series.loc[some_series['Weight'].astype(float).idxmin()][['ObjectName', 'Weight']])
    print("Unknown weight ", count_of_nan)
    dict = {'Object': [some_series.loc[some_series['Weight'].astype(float).idxmin()]['ObjectName'], 'NaN weight'],
            'Weight': [some_series['Weight'].min(), count_of_nan]}
    output = pd.DataFrame(dict)
    output.to_csv('general-stats.csv')


def d():
    data = pd.read_csv('cstmc-CSV-en.csv', sep='|', error_bad_lines=False)
    some_series = data[['ObjectName', 'NumberOfComponents']]
    print(some_series)
    count_of_nan = 0
    for i in some_series.index:
        if str(some_series['NumberOfComponents'][i]) == 'nan':
            count_of_nan += 1
    print(
        some_series.loc[some_series['NumberOfComponents'].astype(float).idxmax()][['ObjectName', 'NumberOfComponents']])
    print("Unknown weight ", count_of_nan)
    dict = {'Object': [some_series.loc[some_series['NumberOfComponents'].astype(float).idxmax()]['ObjectName'],
                       'NaN components'],
            'count': [some_series['NumberOfComponents'].max(), count_of_nan]}
    output = pd.DataFrame(dict)
    output.to_csv('general-stats.csv')


d()
