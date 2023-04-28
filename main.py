from pprint import pprint
import csv
# from file_reader import write_file
import contacts

cb = contacts.Contact_book('phonebook_raw.csv')
cb.write_in_file('final', cb.del_dupls('firstname', 'lastname'))