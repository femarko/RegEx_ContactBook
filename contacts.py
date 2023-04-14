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

    def correct_names_and_phones(self):
        correct_names_and_phones_list= []
        for contact_index, contact in enumerate(self.entries):
            words = re.findall(r'[А-Яёа-яё]+', str(contact))
            for iteration in range(3):  # решение Задачи 1
                if len(words) < iteration + 1:
                    contact[iteration] = ''
                else:
                    contact[iteration] = words[iteration]
            contact[-2] = re.sub(self.reg_ex_patterns.phone_pattern,
                                 self.reg_ex_patterns.subst, contact[-2])
            correct_names_and_phones_list.append(contact)
        return correct_names_and_phones_list

    def entries_dict(self):
        entries_dict = {}
        for header_index, header in enumerate(self.headers):
            values_indicies_list = []
            for entry_index, entry in enumerate(self.correct_names_and_phones()):
                values_indicies_list.append(entry[header_index])
            entries_dict[header] = values_indicies_list
        return entries_dict

    def duplicates_info(self, *fields):
        for field in fields:
            if len(self.entries_dict()[field]) != len(str(set(self.entries_dict()[field]))):
                duplicates_dict = {}
                for element_index, element in enumerate(self.entries_dict()[field]):
                    duplicates_dict[element] = [self.entries_dict()[field].index(element)]
                for element_index, element in enumerate(self.entries_dict()[field]):
                    if element_index != self.entries_dict()[field].index(element):
                        duplicates_dict[element].append(element_index)
                keys_to_delete_list = []
                for key in duplicates_dict.keys():
                    if len(duplicates_dict[key]) == 1:
                        keys_to_delete_list.append(key)
                for key_to_del in keys_to_delete_list:
                    del(duplicates_dict[key_to_del])
        return duplicates_dict

    # def duplicates_del(self):
    #     for key in