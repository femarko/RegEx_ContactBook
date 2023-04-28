import csv
from pprint import pprint

def read_file(file_name):
    with open(file_name, encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        all_data = list(rows)
        headers = all_data[0]
        entries = all_data[1:]
        return all_data, headers, entries

