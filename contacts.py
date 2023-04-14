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

    # def contacts_dict(self):
    #     '''ключи - индексы'''
    #     contacts_dict = {}
    #     for contact_index, contact in enumerate(self.entries):
    #         words = re.findall(r'[А-Яёа-яё]+', str(contact))
    #         for iteration in range(3):  # решение Задачи 1
    #             if len(words) < iteration + 1:
    #                 contact[iteration] = ''
    #             else:
    #                 contact[iteration] = words[iteration]
    #         contact[-2] = re.sub(self.reg_ex_patterns.phone_pattern,
    #                              self.reg_ex_patterns.subst, contact[-2])
    #         contacts_dict[contact_index + 1] = dict(zip(self.headers, contact))  # ключи - индексы
    #     return contacts_dict

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

    def duplicates(self, *fields):
       for field in fields:
           if len(self.entries_dict()[field]) != len(str(set(self.entries_dict()[field]))):
                for element_index, element in enumerate(self.entries_dict()[field]):
                    
                    print(f'element: {element} self.entries_dict()[field].index(element): {self.entries_dict()[field].index(element)} element_index: {element_index}')


        #     print(self.entries_dict()[self.headers[0]])
        #     print(self.entries_dict()[self.headers[1]])
        #
        # for index in range(len(self.entries)):
        #     print(f'{self.entries_dict()[self.headers[0]][index]} {index}')
        # if self.correct_names_and_phones()
        # if len(self.entries_dict()[self.headers[0]]) != lenset((self.entries_dict()[self.headers[0]]))

    '''def _get_duplicates_list_of_tuples(self):
        duplicates_list = []
        for key in self.contacts_dict().keys():
            indeces_list = []
            for index, entry in enumerate(self.all_data):
                if entry[0] == self.contacts_dict()[key]['lastname'] and \
                        entry[1] == self.contacts_dict()[key]['firstname']:
                    indeces_list.append(index)
                    duplicates_list.append(indeces_list)
        duplicates_list_of_tuples = []
        for value in duplicates_list:
            if len(value) > 1:
                duplicates_list_of_tuples.append(tuple(value))
        duplicates_list_of_tuples = list(set(duplicates_list_of_tuples))
        return duplicates_list_of_tuples

    def duplicated_entries(self):
        duplicates_dict = {}
        for tuple_index, tuple_ in enumerate(self._get_duplicates_list_of_tuples()):
            for tuple_element_index, tuple_element in enumerate(tuple_):
                for header in self.headers:
                    duplicates_dict[tuple_index] = {
                        header: [self.contacts_dict()[tuple_element][header], tuple_element]
                    }
        return duplicates_dict'''
