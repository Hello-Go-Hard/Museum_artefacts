import pandas as pd

file_csv = open("cstmc-CSV-en.csv", 'r')
clean_data = []

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

# count in every categories
materials = structuring_data[column_name['material']]
dict_materials = {}
BeginDate_list = structuring_data[column_name['BeginDate']]
set_of_date = set(BeginDate_list)
set_of_date.remove('')
date_to_index_dict = {}
for i in set_of_date:
    date_to_index_dict[i] = [j for j in range(len(BeginDate_list)) if BeginDate_list[j] == i]
date_to_materials_dict = {}
for i in set_of_date:
    materials_dict = {}
    for j in date_to_index_dict[i]:
        for one_material in materials[j].split(';'):
            try:
                materials_dict[one_material] = materials_dict[one_material] + 1
            except KeyError:
                materials_dict[one_material] = 1
    date_to_materials_dict[i] = materials_dict
keys_to_sort = list(date_to_materials_dict.keys())
keys_to_sort.sort()
date = []
material = []
count_of_material = []

date_keys = list(date_to_materials_dict.keys())
date_keys.sort()

for i in date_keys:
    material += list(date_to_materials_dict[i].keys())
    count_of_material += list((date_to_materials_dict[i].values()))
    for j in range(len(date_to_materials_dict[i].keys())):
        date.append(i)
dict_to_file = {'Date': date, 'Material': material, 'Count': count_of_material}
output = pd.DataFrame(dict_to_file)
output.to_csv('material-stats.cvs')
