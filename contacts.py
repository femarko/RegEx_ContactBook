from pprint import pprint
import reg_ex_patterns
import csv
import re
from file_reader import read_file

class Contact_book:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all_data, self.headers, self.entries = read_file(self.file_name)
        self.reg_ex_patterns = reg_ex_patterns

    def read_file(self):
        with open(self.file_name, encoding='utf8') as f:
            rows = csv.reader(f, delimiter=",")
            return list(rows)

    def get_contacts_dict(self):
        contacts_dict = {}
        for contact_index, contact in enumerate(self.entries):
            words = re.findall(r'[А-Яёа-яё]+', str(contact))
            for iteration in range(3):  # решение Задачи 1
                if len(words) < iteration + 1:
                    contact[iteration] = ''
                else:
                    contact[iteration] = words[iteration]
            contact[-2] = re.sub(self.reg_ex_patterns.phone_pattern, self.reg_ex_patterns.subst, contact[-2])  # решение Задачи 2
            contacts_dict[contact_index + 1] = dict(zip(self.headers, contact))
        return contacts_dict

    def remove_duplicates(self):
        duplicates_list = []
        for key in self.get_contacts_dict().keys():
            indeces_list = []
            for index, entry in enumerate(self.all_data):
                if entry[0] == self.get_contacts_dict()[key]['lastname'] and entry[1] == self.get_contacts_dict()[key]['firstname']:
                    indeces_list.append(index)
                    duplicates_list.append(indeces_list)
        duplicates_list_of_tuples = []
        for value in duplicates_list:
            if len(value) > 1:
                duplicates_list_of_tuples.append(tuple(value))
        duplicates_list_of_tuples = list(set(duplicates_list_of_tuples))
        return duplicates_list_of_tuples