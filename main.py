from pprint import pprint
import csv
from file_reader import write_file
import contacts

cb = contacts.Contact_book('phonebook_raw.csv')
pprint(cb.del_dupls('firstname', 'lastname'))
# pprint(contacts_list)

# with open("phonebook.csv", "w", encoding='utf8') as f:
# #     datawriter = csv.writer(f, delimiter=',')
# #
# #     ## Вместо contacts_list подставьте свой список:
# #     datawriter.writerows(contacts)
#
# with open('outputfile.csv', "w", newline='', encoding='utf-8') as f2:
#     f2.writelines(contacts)

