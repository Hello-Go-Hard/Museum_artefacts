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
categories_1 = structuring_data[column_name['category1']]
categories_2 = structuring_data[column_name['category2']]
categories_3 = structuring_data[column_name['category3']]
categories = categories_1 + categories_2 + categories_3
set_of_categories = set(categories)
dict_categories = {}
for i in set_of_categories:
    dict_categories[i] = categories.count(i)
categories, count_of_categories = list(dict_categories.keys()), list(dict_categories.values())

dict_to_file = {"Category": categories, "Count": count_of_categories}
output = pd.DataFrame(dict_to_file)
output.to_csv('object-stats.cvs')
