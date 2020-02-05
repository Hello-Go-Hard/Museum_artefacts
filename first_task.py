import pandas as pd

file_csv = open("cstmc-CSV-en.csv", 'r')
clean_data = []
output_data_column = []
output_data_value = []

for i in file_csv:
    some_artefact = i.split('|')
    if len(some_artefact) != 36:
        some_artefact =some_artefact[:-1]
    clean_data.append(some_artefact)
column_name = {}

for (i, j) in zip(clean_data[0], range(36)):
    column_name[i] = j
structuring_data = []
for j in range(36):
    some_array = []
    for i in clean_data[1:]:
        some_array.append(i[j])
    structuring_data.append(some_array)

# country with max of artefacts
country = structuring_data[column_name['ManuCountry']]
set_of_country = set(country)
unknown_country = ('Unknown', country.count("") + country.count('Unknown'))
set_of_country.remove('')
set_of_country.remove('Unknown')
max_country = ('country', 1)
for i in set_of_country:
    if country.count(i) > max_country[1]:
        max_country = (i, country.count(i))
output_data_column.append(max_country[0])
output_data_value.append(max_country[1])
output_data_column.append(unknown_country[0])
output_data_value.append(unknown_country[1])


# max(BeginDate - Enddate)
BeginDate_list = structuring_data[column_name['BeginDate']]
EndDate_list = structuring_data[column_name['EndDate']]
new_column = []
unknown_date = 0
for (i, j) in zip(BeginDate_list, EndDate_list):
    if i == "" or j == '':
        unknown_date += 1
        new_column.append(0)
        continue
    new_column.append(int(j)-int(i))
unknown_date = ('Unknown', unknown_date)
max_time = max(new_column)
max_time = (country[new_column.index(max_time)], max_time)

output_data_column.append(max_time[0])
output_data_value.append(max_time[1])
output_data_column.append(unknown_date[0])
output_data_value.append(unknown_date[1])

# min(Weight)
Weight_list = structuring_data[column_name['Weight']]
type_of_weight = ['lbs', 'kg', 'Metric tons', 'gm']
convert_weight = {'lbs': 0.453592, 'kg': 1, 'Metric tons': 1000, 'gm': 0.001}
unknown_weight = 0
for i in range(len(Weight_list)):
    if '.' in Weight_list[i] and ',' in Weight_list[i]:
        Weight_list[i] = Weight_list[i][(Weight_list[i].find(',')+1):]
    Weight_list[i] = Weight_list[i].replace(',', '.')

for i in range(len(Weight_list)):
    count_digit = 0
    for j in range(len(Weight_list[i])):
        if Weight_list[i][j].isdigit() or Weight_list[i][j] == '.':
            count_digit += 1
        else:
            if Weight_list[i][j+1].isdigit():
                continue
            else:
                break
    if count_digit == 0:
        unknown_weight += 1
        Weight_list[i] = 1000
    else:
        for id_convert in type_of_weight:
            if id_convert in str(Weight_list[i]):
                convert_value = convert_weight[id_convert]
                digit_weight = float(Weight_list[i][:count_digit])
                Weight_list[i] = convert_value * digit_weight
            if 'cm' in str(Weight_list[i]):
                Weight_list[i] = 1000

min_weight = min(Weight_list)
min_weight = (structuring_data[column_name['ObjectName']][Weight_list.index(min(Weight_list))], min_weight)
unknown_weight = ('Unknown', unknown_weight)

output_data_column.append(min_weight[0])
output_data_value.append(min_weight[1])
output_data_column.append(unknown_weight[0])
output_data_value.append(unknown_weight[1])

# max(NumberOfComponents)
count_of_components = structuring_data[column_name['NumberOfComponents']]
set_of = set(count_of_components)
unknown_components = ("Unknown", count_of_components.count(""))
max_components = (0, 0)
for i in range(len(count_of_components)):
    if count_of_components[i] != '' and int(count_of_components[i]) > int(max_components[1]):
        max_components = (i, count_of_components[i])
max_components = (structuring_data[column_name['ObjectName']][max_components[0]], max_components[1])

output_data_column.append(max_components[0])
output_data_value.append(max_components[1])
output_data_column.append(unknown_components[0])
output_data_value.append(unknown_components[1])
dict_to_file = {"Name": output_data_column, "Value": output_data_value}
output = pd.DataFrame(dict_to_file)
output.to_csv('general-stats.cvs')
