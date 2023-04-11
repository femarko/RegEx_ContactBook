from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re


with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

contacts_dict = {}

for contact_index, contact in enumerate(contacts_list[1:]):
    words = re.findall(r'\w+', str(contact))
    contacts_dict[contact_index] = {'person': dict(zip(contacts_list[0][0:3], words[0:3]))}
pprint(contacts_dict)

