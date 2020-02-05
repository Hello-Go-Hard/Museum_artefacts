import csv

file_csv = open("cstmc-CSV-en.csv", 'r')
clean_data = []
output_data_column = []
output_data_value = []

for one_string in file_csv:
    some_artifact = one_string.split('|')
    if len(some_artifact) != 36:
        some_artifact = some_artifact[:-1]
    clean_data.append(some_artifact)
column_names = {}

for (column_name, index) in zip(clean_data[0], range(36)):
    column_names[column_name] = index
structuring_data = []
for index in range(36):
    some_array = []
    for one_string in clean_data[1:]:
        some_array.append(one_string[index])
    structuring_data.append(some_array)

# count in every categories
materials = structuring_data[column_names['material']]
dict_materials = {}
begin_date_list = structuring_data[column_names['BeginDate']]
set_of_date = set(begin_date_list)
set_of_date.remove('')
date_to_index_dict = {}
for date in set_of_date:
    date_to_index_dict[date] = [index_date for index_date in range(len(begin_date_list)) if begin_date_list[index_date] == date]
date_to_materials_dict = {}
for date in set_of_date:
    materials_dict = {}
    for index in date_to_index_dict[date]:
        for one_material in materials[index].split(';'):
            try:
                materials_dict[one_material] = materials_dict[one_material] + 1
            except KeyError:
                materials_dict[one_material] = 1
    date_to_materials_dict[date] = materials_dict
keys_to_sort = list(date_to_materials_dict.keys())
keys_to_sort.sort()
date = []
material = []
count_of_material = []

date_keys = list(date_to_materials_dict.keys())
date_keys.sort()

for one_date in date_keys:
    material += list(date_to_materials_dict[one_date].keys())
    count_of_material += list((date_to_materials_dict[one_date].values()))
    for j in range(len(date_to_materials_dict[one_date].keys())):
        date.append(one_date)
file_csv.close()

file_output = open('material-stats.csv', 'w', newline='')
writer = csv.DictWriter(file_output, fieldnames=['Date', 'Material', 'Count'])
writer.writeheader()
for (one_date, one_material, one_count) in zip(date, material, count_of_material):
    writer.writerow({'Date': one_date, 'Material': one_material, 'Count': one_count})
file_output.close()
