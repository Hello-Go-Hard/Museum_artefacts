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

# country with max of artifacts
countries = structuring_data[column_names['ManuCountry']]
set_of_country = set(countries)
unknown_country = ('Unknown', countries.count("") + countries.count('Unknown'))
set_of_country.remove('')
set_of_country.remove('Unknown')
max_country = ('country', 1)
for one_country in set_of_country:
    if countries.count(one_country) > max_country[1]:
        max_country = (one_country, countries.count(one_country))
output_data_column.append(max_country[0])
output_data_value.append(max_country[1])
output_data_column.append(unknown_country[0])
output_data_value.append(unknown_country[1])


# max(begin_date - end_date)
begin_date_list = structuring_data[column_names['BeginDate']]
end_date_list = structuring_data[column_names['EndDate']]
new_column = []
unknown_date = 0
for (date_of_begin, date_of_end) in zip(begin_date_list, end_date_list):
    if date_of_begin == "" or date_of_end == '':
        unknown_date += 1
        new_column.append(0)
        continue
    new_column.append(int(date_of_end)-int(date_of_begin))
unknown_date = ('Unknown', unknown_date)
max_time = max(new_column)
max_time = (countries[new_column.index(max_time)], max_time)

output_data_column.append(max_time[0])
output_data_value.append(max_time[1])
output_data_column.append(unknown_date[0])
output_data_value.append(unknown_date[1])

# min(Weight)
Weight_list = structuring_data[column_names['Weight']]
type_of_weight = ['lbs', 'kg', 'Metric tons', 'gm']
convert_weight = {'lbs': 0.453592, 'kg': 1, 'Metric tons': 1000, 'gm': 0.001}
unknown_weight = 0
for index in range(len(Weight_list)):
    if '.' in Weight_list[index] and ',' in Weight_list[index]:
        Weight_list[index] = Weight_list[index][(Weight_list[index].find(',')+1):]
    Weight_list[index] = Weight_list[index].replace(',', '.')

for index in range(len(Weight_list)):
    count_digit = 0
    for second_index in range(len(Weight_list[index])):
        if Weight_list[index][second_index].isdigit() or Weight_list[index][second_index] == '.':
            count_digit += 1
        else:
            if Weight_list[index][second_index+1].isdigit():
                continue
            else:
                break
    if count_digit == 0:
        unknown_weight += 1
        Weight_list[index] = 1000
    else:
        for id_convert in type_of_weight:
            if id_convert in str(Weight_list[index]):
                convert_value = convert_weight[id_convert]
                digit_weight = float(Weight_list[index][:count_digit])
                Weight_list[index] = convert_value * digit_weight
            if 'cm' in str(Weight_list[index]):
                Weight_list[index] = 1000

min_weight = min(Weight_list)
min_weight = (structuring_data[column_names['ObjectName']][Weight_list.index(min(Weight_list))], min_weight)
unknown_weight = ('Unknown', unknown_weight)

output_data_column.append(min_weight[0])
output_data_value.append(min_weight[1])
output_data_column.append(unknown_weight[0])
output_data_value.append(unknown_weight[1])

# max(NumberOfComponents)
count_of_components = structuring_data[column_names['NumberOfComponents']]
set_of = set(count_of_components)
unknown_components = ("Unknown", count_of_components.count(""))
max_components = (0, 0)
for index in range(len(count_of_components)):
    if count_of_components[index] != '' and int(count_of_components[index]) > int(max_components[1]):
        max_components = (index, count_of_components[index])
max_components = (structuring_data[column_names['ObjectName']][max_components[0]], max_components[1])

output_data_column.append(max_components[0])
output_data_value.append(max_components[1])
output_data_column.append(unknown_components[0])
output_data_value.append(unknown_components[1])
file_csv.close()

file_output = open('general-stats.csv', 'w', newline='')
writer = csv.DictWriter(file_output, fieldnames=['Name', 'Value'])
writer.writeheader()
for (column, value) in zip(output_data_column, output_data_value):
    writer.writerow({'Name': column, 'Value': value})
file_output.close()
