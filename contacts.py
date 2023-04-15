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
        duplicates_dict = {}
        if len(fields) == 0:
            fields_to_check = self.headers
        else:
            fields_to_check = fields
        for field in fields_to_check:
            duplicates_dict.setdefault(field, {})
            if len(self.entries_dict()[field]) != len(str(set(self.entries_dict()[field]))):
                for element_index, element in enumerate(self.entries_dict()[field]):
                    duplicates_dict[field][element] = [self.entries_dict()[field].index(element)]
                for element_index, element in enumerate(self.entries_dict()[field]):
                    if element_index != self.entries_dict()[field].index(element):
                        duplicates_dict[field][element].append(element_index)
                keys_to_delete_list = []
                for key in duplicates_dict.keys():
                    for key_element in duplicates_dict[key].keys():
                        if len(duplicates_dict[key][key_element]) == 1:
                            keys_to_delete_list.append(key_element)
                    for key_to_del in keys_to_delete_list:
                        del (duplicates_dict[key][key_to_del])
        return duplicates_dict

    # def duplicates_del(self, *fields):
    #     if len(fields) == 0:
    #         fields_to_check = self.headers
    #     else:
    #         fields_to_check = fields
    #     list_of_lists_of_duplicated_entries_indicies = []
    #     for field in fields_to_check: # уровень поля
    #         list_of_entries_with_duplicates_within_the_field = []
    #         duplicates_of_one_value = []
    #         for key in self.duplicates_info()[field].keys(): # уровень дублированных значений внутри поля
    #             duplicates_of_one_value.append(self.duplicates_info()[field][key]) # кладем список номеров дублир записей для одного значения в список
    #         list_of_entries_with_duplicates_within_the_field.append(duplicates_of_one_value)
    #     list_of_lists_of_duplicated_entries_indicies.append(list_of_entries_with_duplicates_within_the_field)
    #     return list_of_lists_of_duplicated_entries_indicies

    def duplicates_del(self, *fields, **fields_pairs):
        general_list = []
        '''
        для каждого field (фамилия) - получаем список номеров (их может быть несколько)
        по каждому номеру из списка проверяем, совпадает ли его имя с именем этого номера 
        в каждом списке каждый номер сравнить с этим же номером но другим field
        :param fields: 
        :return: 
        '''
        for field_index, field in enumerate(fields):
            field_dict = {field:[]}
            for key in self.duplicates_info()[field].keys(): # <- список ключей к спискам номеров записей
                # field_list.append({field: self.duplicates_info()[field][key]})
                field_dict[field].append(self.duplicates_info()[field][key])
            general_list.append(field_dict)
        return general_list

