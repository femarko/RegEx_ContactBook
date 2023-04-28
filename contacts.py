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

    def header_index_entry(self):
        entries_dict = {}
        for header_index, header in enumerate(self.headers):
            entries_dict[header] = {}
            for entry_index, entry in enumerate(self.correct_names_and_phones()):
                entries_dict[header][entry_index] = entry[header_index]
        return entries_dict

    def dupl_dict(self, *fields):
        if len(fields) != 0:
            fields_to_check = fields
        else:
            fields_to_check = self.headers
        dupl_dict = {}
        for header in fields_to_check:
        # for header, entries in self.header_index_entry().items():
            if len(self.entries_dict()[header]) != len(set(self.entries_dict()[header])):
                dupl_dict[header] = {}
                for entry_index, entry in enumerate(self.entries_dict()[header]):
                    if entry_index != self.entries_dict()[header].index(entry):
                        dupl_dict[header][self.entries_dict()[header].index(entry)] = []
                        dupl_dict[header][self.entries_dict()[header].index(entry)].append(self.entries_dict()[header].index(entry))
                for entry_index, entry in enumerate(self.entries_dict()[header]):
                    if entry_index != self.entries_dict()[header].index(entry):
                        dupl_dict[header][self.entries_dict()[header].index(entry)].append(entry_index)
        return dupl_dict

    def dupl_bul(self, *fields):
        dupl_dict = self.dupl_dict(*fields)
        key_0 = list(dupl_dict.keys())[0]
        result = True
        while result == True:
            for key in list(dupl_dict.keys())[1:]:
                if dupl_dict[key] == dupl_dict[key_0]:
                    result = True
                else:
                    result = False
            break
        return result, dupl_dict[key_0]

    def entries_numbers_delition_list(self, *fields):
        if self.dupl_bul(*fields)[0] == False:
            return f'Not all entries are duplicated in the requested fields'
        else:
            entries_numbers_delition_list = []
            dict_ = self.dupl_bul(*fields)[1]
            for value in dict_.values():
                entries_numbers_delition_list.append(value)
        return entries_numbers_delition_list

    def delition_list(self, *fields):
        list_ = self.entries_numbers_delition_list(*fields)
        dict_ = self.entries_dict()
        delition_list = []
        for list_index, list_of_indeces in enumerate(list_):
            delition_list.append([])
            for index in list_of_indeces[1:]:
                for header in self.headers:
                    if len(self.header_index_entry()[header][index]) <= \
                            len(self.header_index_entry()[header][list_of_indeces[0]]):
                        delition_list[list_index].append({header: index})
                    else:
                        delition_list[list_index].append({header: list_of_indeces[0]})
        return delition_list

    def clear_dict(self, *fields):
        delition_list = self.delition_list(*fields)
        auxiliary_dict = self.header_index_entry()
        clear_dict = {}
        for list_ in delition_list:
            for dict_ in list_:
                for key, value in dict_.items():
                    del(auxiliary_dict[key][value])
        for key_, value_ in auxiliary_dict.items():
            for value__ in value_.values():
                clear_dict[key_] = list(value_.values())
        return clear_dict

    def del_dupls(self, *fields):
        clear_dict = self.clear_dict(*fields)
        entries_qwantity = len(list(clear_dict.values())[0])
        clear_list = []
        clear_list.append(self.headers)
        for number in range(entries_qwantity):
            auxiliary_list = []
            for key, value in clear_dict.items():
                auxiliary_list.append(clear_dict[key][number])
            clear_list.append(auxiliary_list)
        return clear_list

    def write_in_file(self, name_of_final_file, list_to_be_written):
        with open(name_of_final_file, "w", encoding='utf8') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(list_to_be_written)