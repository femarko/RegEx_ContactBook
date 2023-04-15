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
        Возвращается словарь duplicates_dict.

        Параметры:
        - на вход принимается любое количество заголовков телефонной книги
        - если параметры не переданы, обрабатываются все заголовки телефонной книги.

        Обработка заголовков (fields):
        - если длина списка, полученного по ключу field из словаря self.entries_dict(), не равна длине
          множества, полученного из этого списка (проверка наличия повторяющихся элементов), field
          становится ключом словаря duplicates_dict.

        Словарь duplicates_dict:
        - ключи - полученные аргументы (field in fields) - обрабатываемые заголовки телефонной книги
        - значения - вложенные словари, в которых:
            - ключи - элементы списка, полученного по ключу обрабатываемого заголовка (field) из словаря
              self.entries_dict() (список из словаря self.entries_dict())
            - значения - списки всех вхождеий (индексов) повторящихся элементов указанного списка
              из словаря self.entries_dict()
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

    def duplicates_merge(self, *fields):
        '''
    1. Получить сравниваемые поля (*fields)
	2. Первое поле (fields[0]) сравнить с остальными (for field in fields[1:]:):
	    -равен ли каждый из вложенных списков первого поля вложенным спискам остальных полей?
	for nested_list in
	(if self.duplicates_compare()[field][nested_list]==self.duplicates_compare[fields[0]][nested_list])
	Если да: zip(self.entries_dict()[field[0]][nested_list], self.duplicates_compare()[field][nested_list])
    Результат zip записываем в список
        '''
        # list_1 = self.duplicates_compare()[field_1]
        # list_2 = self.duplicates_compare()[field_2]
        # entries_to_merge_list = []
        # for pare_of_entries in list_1:
        #     pare_of_entries_list = []
        #     if list_2[list_1.index(pare_of_entries)] == pare_of_entries:
        #         pare_of_entries_list.append(pare_of_entries)
        #     entries_to_merge_list.append(pare_of_entries)
        # pprint(entries_to_merge_list)
        #
        #
        # if entries_to_merge_list:
        #     list_to_zip = []
        #     for list_ in entries_to_merge_list:
        #         print(f'list_ {type(list_)} {list_}')
        #         entries_to_merge = []
        #         for entry_index in list_:
        #             entries_to_merge.append(self.entries[entry_index])
        #         list_to_zip.append(entries_to_merge)
        #
        # else:
        #     return
        # pprint((list_to_zip))
        #
        #
        # zipped = []
        # if list_to_zip:
        #
        #     for item in list_to_zip:
        #         for el in item:
        #             zipped.append(zip(item))
        # print(zipped)
        #
        # for i in zipped[0]:
        #     print(i)
        if len(fields) == 0:
            fields_to_check = self.headers
        else:
            fields_to_check = fields
            # first_argument = fields[0]

        for field in fields_to_check[1:]: # итерируемся по кортежу аргументов, кроме первого аргумента
            for num, nested_list in enumerate(self.duplicates_compare()[fields[0]]): # итерируемся по списку из [field_to_check]
                if self.duplicates_compare()[field][num] == self.duplicates_compare()[fields[0]][num]:
                    tuples_list = []
                    for position, index_ in enumerate(nested_list):  # итерируемся по вложенному списку - создаем список кортежей
                        print(self.entries_dict()[fields[0]][index_])
                        print(self.entries_dict()[field][self.duplicates_compare()[field][num][position]])
                        # tuples_list.append(
                        #     zip(self.entries_dict()[fields[0]][index_], self.entries_dict()[self.duplicates_compare()[field][num][index_]])
                        # )
                        # print(tuples_list)





