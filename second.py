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
categories_1 = structuring_data[column_names['category1']]
categories_2 = structuring_data[column_names['category2']]
categories_3 = structuring_data[column_names['category3']]
categories = categories_1 + categories_2 + categories_3
set_of_categories = set(categories)
dict_categories = {}
for category in set_of_categories:
    dict_categories[category] = categories.count(category)
categories, count_of_categories = list(dict_categories.keys()), list(dict_categories.values())
file_csv.close()

file_output = open('object-stats.csv', 'w', newline='')
writer = csv.DictWriter(file_output, fieldnames=['Category', 'Count'])
writer.writeheader()
for (category, count_of_category) in zip(categories, count_of_categories):
    writer.writerow({'Category': category, 'Count': count_of_category})
file_output.close()
