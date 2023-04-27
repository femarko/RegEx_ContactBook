import csv
from pprint import pprint

def read_file(file_name):
    with open(file_name, encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        all_data = list(rows)
        headers = all_data[0]
        entries = all_data[1:]
        return all_data, headers, entries

def write_file(file_name_1, file_name_2):
    with open(file_name_1, "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)