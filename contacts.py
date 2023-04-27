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

    def new_header_index_entry(self):
        entries_dict = {}
        for header_index, header in enumerate(self.headers):
            entries_dict[header] = {}
            for entry_index, entry in enumerate(self.correct_names_and_phones()):
                entries_dict[header][entry_index] = entry[header_index]
        return entries_dict

    def new_dupl_dict(self, *fields):
        if len(fields) != 0:
            fields_to_check = fields
        else:
            fields_to_check = self.headers
        dupl_dict = {}
        for header in fields_to_check:
        # for header, entries in self.new_header_index_entry().items():
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

    def new_dupl_bul(self, *fields):
        dupl_dict = self.new_dupl_dict(*fields)
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

    def new_entries_numbers_delition_list(self, *fields):
        if self.new_dupl_bul(*fields)[0] == False:
            return f'Not all entries are duplicated in the requested fields'
        else:
            entries_numbers_delition_list = []
            dict_ = self.new_dupl_bul(*fields)[1]
            for value in dict_.values():
                entries_numbers_delition_list.append(value)
        return entries_numbers_delition_list

    def new_del_dupls(self, *fields):
        list_ = self.new_entries_numbers_delition_list(*fields)
        dict_ = self.entries_dict()
        delition_list = []
        for list_index, list_of_indeces in enumerate(list_):
            delition_list.append([])
            for index in list_of_indeces[1:]:
                for header in self.headers:
                    if len(self.new_header_index_entry()[header][index]) <= \
                            len(self.new_header_index_entry()[header][list_of_indeces[0]]):
                        delition_list[list_index].append({header: index})
                    else:
                        delition_list[list_index].append({header: list_of_indeces[0]})
        return delition_list
            #     list_to_del.append(dict_[key][item])




        # dupl_group_numbers_list = []
        # for header, indeces_dict in dupl_dict.items():
        #     for key, value in indeces_dict.items():
        #         dupl_group_numbers_list.append(key)
        # return list(set(dupl_group_numbers_list))





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
            for key in self.duplicates_info(fields_to_check)[field].keys():
                field_list.append(self.duplicates_info()[field][key])
            duplicates_dict.setdefault(field, field_list)
        return duplicates_dict

    def _del_dict(self, *fields):
        '''
    Возвращает словарь, где ключи - поля телефонной книги, значения - списки индексов записей, подлежащих удалению в
    соответствующем поле.
        '''
        duplicates_dict = self.duplicates_compare(*fields)
        if len(fields) == 0:
            fields_to_check = self.headers
        else:
            fields_to_check = fields
        print(f'fields_to_check {fields_to_check}')

        count = 0
        for field in fields_to_check[1:]: # итерируемся по кортежу аргументов, кроме первого аргумента
            for num, nested_list in enumerate(self.duplicates_compare()[fields_to_check[0]]): # итерируемся по списку из fields_to_check
                if self.duplicates_compare(fields_to_check)[field][num] == self.duplicates_compare(fields_to_check)[fields_to_check[0]][num]:
                    print(self.duplicates_compare()[field][num])
                    count += 1
                    continue
                else:
                    break
        if count < len(fields[1:]):
            print('Not all requested entries are duplicated.')
            return
        else:
            result = True
        print(result)
        print(f'duplicates_dict {type(duplicates_dict)} {duplicates_dict}')
        if result:
            indeces = self.duplicates_compare()[fields_to_check[0]] # т.к. вложенные списки совпали для всех полей, берем первое (field[0])
            the_list = []
        #     for header in self.entries_dict().keys():
        #         nestedval = []
        #         the_list.append(nestedval)
        #         for nested_list in indeces:
        #             indexval = []
        #             nestedval.append(indexval)
        #             for index in nested_list:
        #                 indexval.append(self.entries_dict()[header][index])
        #
        #     indeces_dict = {}
        #
        #     for field_index, field_values in enumerate(the_list):
        #         indeces_dict[self.headers[field_index]] = {}
        #         for nested_list_index, nested_list in enumerate(field_values):
        #             indeces_dict[self.headers[field_index]][nested_list_index] = []
        #             for entry_value_index, entry_value in enumerate(nested_list):
        #                 indeces_dict[self.headers[field_index]][nested_list_index].append(len(entry_value))
        #
        #     for key in indeces_dict.keys():
        #         for key_nest, value in indeces_dict[key].items():
        #             for length in indeces_dict[key][key_nest]:
        #                 if length == max(value):
        #                     indeces_dict[key][key_nest] = value.index(length)
        #
        #     del_dict = {}
        #     for header in self.headers:
        #         del_dict[header] = []
        #         for num_list_, list_ in enumerate(indeces):
        #             for entr in list_:
        #                 if list_.index(entr) != indeces_dict[header][num_list_]:
        #                     del_dict[header].append(entr)
        #     return del_dict
    def target(self, *fields):
        del_dict = self._del_dict(*fields)
        pprint(del_dict)
        # pure_dict = {}
        # pprint(pure_dict)
        # for contact_field, list_to_del in del_dict.items():
        #     list_for_contact_field = self.entries_dict()[contact_field].pop(list_to_del[0])
        #     for item in list_to_del[1:]:
        #         list_for_contact_field.append(self.entries_dict().pop(item))
        #
        #
        # return pure_dict

    # def accept(self, *fields):
    #     fields_list = []
    #     for field in fields:
    #         fields_list.append(field)
    #     return fields_list
    #
    # def exp(self, *fields):
    #     print(self.accept(*fields))