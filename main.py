from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

phone_number_pattern = r'(\+7|8)?[\s(-]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s)*[\s(]*([(])*([доб\.]*)\s*(\d*)[)]*'
subst = r'+7(\2)\3-\4-\5\6\8\9'

for contact_index, contact in enumerate(contacts_list[1:]):
    words = re.findall(r'[А-Яёа-яё]+', str(contact))
    for iteration in range(3):
        if len(words) < iteration + 1:
            contact[iteration] = ''
        else:
            contact[iteration] = words[iteration]
    contacts_list[contact_index][-2] = re.sub(phone_number_pattern, subst, str(contact[-2]))
pprint(contacts_list)
