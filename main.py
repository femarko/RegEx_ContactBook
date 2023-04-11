from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

# 1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно
for contact in contacts_list[1:]:
    words = re.findall(r'[А-Яёа-яё]+', str(contact))
    for iteration in range(3):
        if len(words) < iteration + 1:
            contact[iteration] = ''
        else:
            contact[iteration] = words[iteration]
pprint(contacts_list)
