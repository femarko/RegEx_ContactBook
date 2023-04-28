from pprint import pprint
import csv
import contacts

cb = contacts.Contact_book('phonebook_raw.csv')
cb.write_in_file('phonebook.csv', cb.del_dupls('firstname', 'lastname'))