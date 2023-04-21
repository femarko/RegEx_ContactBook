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
        '''
        Возвращается словарь duplicates_dict, в котором:
        - ключи - это полученные аргументы (field in fields) - обрабатываемые заголовки телефонной книги
        - значения - вложенные словари, в которых:
            - ключи - те значения поля (field), которые повторяются в двух и более записях телефонной книги
            - значения - списки всех вхождеий (индексов) повторящихся значений поля

        Параметры:
        - на вход принимается любое количество заголовков телефонной книги
        - если параметры не переданы, обрабатываются все заголовки телефонной книги (список, хранящийся в атрибуте
          self.headers)

        Обработка заголовков (fields):
        - если длина списка, полученного по ключу field из словаря, возвращаемого функцией self.entries_dict(), не равна
          длине множества, полученного из этого списка (проверка наличия повторяющихся элементов), field становится
          ключом словаря duplicates_dict.
        '''
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

    def duplicates_compare(self, *fields):
        '''
        Возвращается словарь duplicates_dict. В отличие от self.duplicates_info, значением ключа этого
        словаря является список списков. Каждый вложенный список состоит из вхождений (индексов)
        повторяющихся элементов списка, полученного по ключу field из словаря self.entries_dict().
        '''
        if len(fields) == 0:
            fields_to_check = self.headers
        else:
            fields_to_check = fields
        duplicates_dict = {}
        for field in fields_to_check:
            field_list = []
            for key in self.duplicates_info()[field].keys():
                field_list.append(self.duplicates_info()[field][key])
            duplicates_dict.setdefault(field, field_list)
        return duplicates_dict

    def duplication_per_fields(self, *fields):
        '''
    Возвращает словарь, где ключи - индексы полей в словаре self.
        '''
        if len(fields) == 0:
            fields_to_check = self.headers
        else:
            fields_to_check = fields

        for field in fields_to_check[1:]: # итерируемся по кортежу аргументов, кроме первого аргумента
            for num, nested_list in enumerate(self.duplicates_compare()[fields[0]]): # итерируемся по списку из [fields_to_check]
                if self.duplicates_compare()[field][num] == self.duplicates_compare()[fields[0]][num]:
                    result = True
                else:
                    return f'Entries with values, duplicated in all requested fields, are not found.'

        if result:
            indeces = self.duplicates_compare()[fields[0]] # т.к. вложенные списки совпали для всех полей, берем первое (field[0])
            the_list = []
            # iteration = 0
            for header in self.entries_dict().keys():
                nestedval = []
                the_list.append(nestedval)
                # print(f'iteration:{iteration} header:{header} nestedval:{nestedval} the_list:{the_list}')
                for nested_list in indeces:
                    indexval = []
                    nestedval.append(indexval)
                    # print(f'\t\t - nested_list:{nested_list} indexval:{indexval} nestedval:{nestedval}')
                    for index in nested_list:
                        indexval.append(self.entries_dict()[header][index])
                        # print(f'\t\t\tindex:{index} indexval:{indexval}')
                # iteration += 1
            # pprint(the_list)

        print(f'indeces: {indeces}')
        print(f'the_list: {the_list}')
        # f_list = []
        dicttt = {}

        for field_index, field_values in enumerate(the_list):
            dicttt[self.headers[field_index]] = {}
            for nested_list_index, nested_list in enumerate(field_values):
                dicttt[self.headers[field_index]][nested_list_index] = []
                for entry_value_index, entry_value in enumerate(nested_list):
                    dicttt[self.headers[field_index]][nested_list_index].append(len(entry_value))

        pprint(dicttt)

        for key in dicttt.keys():
            for key_nest, value in dicttt[key].items():
                for length in dicttt[key][key_nest]:
                    if length == max(value):
                        dicttt[key][key_nest] = value.index(length)

        del_dict = {}
        for header in self.headers:
            del_dict[header] = []
            for num_list_, list_ in enumerate(indeces):
                # print(list_)
                for entr in list_:
                    if list_.index(entr) != dicttt[header][num_list_]:
                        del_dict[header].append(entr)
        # deletion_dict = {}
        # for ind, list_of_indeces in indeces:
        #     for header in self.headers:
        #         for list_ in indeces:
        #
        #         deletion_dict[header] =
        # final_dict = {}
        # for key in dicttt.keys():
        #     final_dict[key] = []
        #     for key_nest, value in dicttt[key].items():
        #         max_length = max(value)
        #         print(value)
        #         for length in dicttt[key][key_nest]:
        #             if length == max_length and value.index(length) == 0:
        #                 continue
        #             else:
        #                 final_dict[key].append(length)

        # for key in dicttt.keys():
        #     final_dict[key] = []
        #     for nested_length in dicttt.values():
        #         print(nested_length)
                # max_nested_length = max(nested_length)
                # for length in nested_length:
                #     if length == max_nested_length and nested_length.index(length) == 0:
                #         continue
                #     else:
                #         final_dict[key].append(length)



        # final_dict = {}
        #
        # for key, value in dicttt.items():
        #     final_dict[key] = []
        #     for key_n, value_n in value.items():
        #         max_length = max(dicttt[key][key_n])
        #         final_dict[key] = [value_n]
        #         pprint(final_dict)
        #         # print(max_length)
                # for length in dicttt[key][key_n]:
                #     # print(f'{key} {key_n} {length}')
                #     # if len(set(dicttt[key][key_n])) == len(dicttt[key][key_n]):
                #     if length != max_length:
                #             final_dict[key][value_n].append(indeces[key_n][(dicttt[key][key_n].index(length))])
                #     else:
                #         final_dict[key][value_n.append(indeces[key_n][0])
                # pprint(final_dict)

        return del_dict

