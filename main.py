from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# 1. Выполните пункты 1-3 задания.
name_pattern = r'\w+'
names_list = []
for contact in contacts_list[1:]:
    words = re.findall(name_pattern, str(contact))
    names_list.append(words[0:3])
pprint(names_list)

for name in names_list:
    print(name)
'''
если contact[0] не содержит запятых...; если содержит только одну...; если содержит две - ничего не делать
если 
'''


# re.compile(r'')

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
# with open("phonebook.csv", "w") as f:
#     datawriter = csv.writer(f, delimiter=',')
#
#     ## Вместо contacts_list подставьте свой список:
#     datawriter.writerows(contacts_list)
