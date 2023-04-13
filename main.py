from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

phone_pattern = r'(\+7|8)?[\s(-]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s)*[\s(]*([(])*([доб\.]*)\s*(\d*)[)]*'
subst = r'+7(\2)\3-\4-\5\6\8\9'

contacts_dict = {}
for contact_index, contact in enumerate(contacts_list[1:]):
    words = re.findall(r'[А-Яёа-яё]+', str(contact))
    for iteration in range(3):  # решение Задачи 1
        if len(words) < iteration + 1:
            contact[iteration] = ''
        else:
            contact[iteration] = words[iteration]
    contact[-2] = re.sub(phone_pattern, subst, contact[-2])  # решение Задачи 2
    contacts_dict[contact_index + 1] = dict(zip(contacts_list[0], contact))

# решение Задачи 3
'''ПОЛУЧАЕМ ИНДЕКСЫ ДУБЛИРУЮЩИХСЯ ЗАПИСЕЙ (В ВИДЕ КОРТЕЖЕЙ)'''
duplicates_list = []
for key in contacts_dict.keys():
    indeces_list = []
    for index, entry in enumerate(contacts_list):
        if entry[0] == contacts_dict[key]['lastname'] and entry[1] == contacts_dict[key]['firstname']:
            indeces_list.append(index)
            duplicates_list.append(indeces_list)
duplicates_list_of_tuples = []
for value in duplicates_list:
    if len(value) > 1:
        duplicates_list_of_tuples.append(tuple(value))
duplicates_list_of_tuples = list(set(duplicates_list_of_tuples))
print(duplicates_list_of_tuples)

# '''СОЗДАЕМ СПИСОК ДУБЛИРУЮЩИХСЯ ЗАПИСЕЙ (СПИСОК СПИСКОВ)'''
# duplicated_entries_dict = {}
# for duplicate in duplicates_list_of_tuples:
#     auxiliary_list = []
#     for element in range(len(duplicate)):
#         auxiliary_list.append(contacts_list[duplicate[element]])
#     duplicated_entries_dict.setdefault(auxiliary_list)
# # pprint(duplicated_entries_list)
duplicates_dict = {}
for index, duplicate in enumerate(duplicates_list_of_tuples):
    auxiliary_list = []
    for element in duplicate:
        # l.append(contacts_dict[duplicate[element]])
        auxiliary_list.append({element: contacts_dict[element]})
    duplicates_dict[index] = auxiliary_list
# pprint(duplicates_dict)

