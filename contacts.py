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
        '''
        Возвращает списк с исправленными именами, фамилиями и телефонами.
        '''
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

    def _entries_dict(self):
        '''
        Возвращает словарь, где:
        - ключ - заголовок поля (элемент первой строки исходного файла),
        - значение ключа - список значений соответствующего поля из всех записей.
        '''
        entries_dict = {}
        for header_index, header in enumerate(self.headers):
            values_indicies_list = []
            for entry_index, entry in enumerate(self.correct_names_and_phones()):
                values_indicies_list.append(entry[header_index])
            entries_dict[header] = values_indicies_list
        return entries_dict

    def _header_index_entry(self):
        '''
        Возвращает словарь, где:
        - ключ - заголовок поля (элемент первой строки исходного файла),
        - значение - словарь, где:
            - ключ - индекс записи в списке всех записей,
            - значение ключа - значение соответствующего поля из всех записей.
        '''
        entries_dict = {}
        for header_index, header in enumerate(self.headers):
            entries_dict[header] = {}
            for entry_index, entry in enumerate(self.correct_names_and_phones()):
                entries_dict[header][entry_index] = entry[header_index]
        return entries_dict

    def _dupl_dict(self, *fields):
        '''
        Параметры: заголовки полей (если ни один заголовок не передан, обрабатываются все заголовки).
        Возвращает словарь дублируюихся записей, где:
        - ключ - заголовок поля (элемент первой строки исходного файла),
        - значение - словарь, где:
            - значение ключа - список индексов записей, имеющих одинаковое значение в поле, являющися ключом внешнего словаря,
            - ключ - первый  элемент из списка, являющегося значением ключа.
        '''
        if len(fields) != 0:
            fields_to_check = fields
        else:
            fields_to_check = self.headers
        dupl_dict = {}
        for header in fields_to_check:
            if len(self._entries_dict()[header]) != len(set(self._entries_dict()[header])):
                dupl_dict[header] = {}
                for entry_index, entry in enumerate(self._entries_dict()[header]):
                    if entry_index != self._entries_dict()[header].index(entry):
                        dupl_dict[header][self._entries_dict()[header].index(entry)] = []
                        dupl_dict[header][self._entries_dict()[header].index(entry)].append(self._entries_dict()[header].index(entry))
                for entry_index, entry in enumerate(self._entries_dict()[header]):
                    if entry_index != self._entries_dict()[header].index(entry):
                        dupl_dict[header][self._entries_dict()[header].index(entry)].append(entry_index)
        return dupl_dict

    def _dupl_bul(self, *fields):
        '''
        Параметры: заголовки полей (если ни один заголовок не передан, обрабатываются все заголовки).
        Возвращает кортеж из двух элементов, где:
        - первый елемент - булево значение:
            - True - если для каждого обрабатываемого поля найдены записи с одинаковым значением в этом поле,
            - False - в остальных случаях;
        - второй элемент - словарь, где:
            - количество пар "ключ-значение" соответствует количеству полей, для которых найдены записи с одинаковым
            - значением в соответствующем поле,
            - значение ключа - список индексов записей с одинаковым значением в соответствующем поле,
            - ключ - первый элемент списка.
    '''
        dupl_dict = self._dupl_dict(*fields)
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

    def _entries_numbers_delition_list(self, *fields):
        '''
        Параметры: заголовки полей (если ни один заголовок не передан, обрабатываются все заголовки).
        Проверяет, для всех ли переданных заголовков полей найдены записи с повторяющимися значениями в соответствующем поле.
        При отрицательном ответе возвращает f-строку с соответствующим предупреждением.
        При положительном ответе возвращает список списков, где:
         - количество вложенных списков соответствует количеству полей, для которых найдены записи с одинаковым
           значением в соответствующем поле,
         - вложенные списики содержат индексы записей с одинаковым значением в соответствующем поле.
        '''
        if self._dupl_bul(*fields)[0] == False:
            return f'Not all entries are duplicated in the requested fields'
        else:
            entries_numbers_delition_list = []
            dict_ = self._dupl_bul(*fields)[1]
            for value in dict_.values():
                entries_numbers_delition_list.append(value)
        return entries_numbers_delition_list

    def _delition_list(self, *fields):
        '''
        Параметры: заголовки полей (если ни один заголовок не передан, обрабатываются все заголовки).
        Возвращает список списков, где:
        - количество вложенных список соответствует количеству полей, для которых найдены записи с одинаковым
          значением в соответствующем поле,
        - элементами каждого вложенного списика являются словари, где:
            - ключ - заголовок поля,
            - значение - индекс записи, которую нужно удалить, чтобы исключить дублирование.
        '''
        list_ = self._entries_numbers_delition_list(*fields)
        dict_ = self._entries_dict()
        delition_list = []
        for list_index, list_of_indeces in enumerate(list_):
            delition_list.append([])
            for index in list_of_indeces[1:]:
                for header in self.headers:
                    if len(self._header_index_entry()[header][index]) <= \
                            len(self._header_index_entry()[header][list_of_indeces[0]]):
                        delition_list[list_index].append({header: index})
                    else:
                        delition_list[list_index].append({header: list_of_indeces[0]})
        return delition_list

    def _clear_dict(self, *fields):
        '''
        Параметры: заголовки полей (если ни один заголовок не передан, обрабатываются все заголовки).
        Возвращает словарь, где:
        - ключи - заголовки полей;
        - значения - списки значений соответствующего поля в каждой записи, где удалены дублирущиеся значения.
        '''
        delition_list = self._delition_list(*fields)
        auxiliary_dict = self._header_index_entry()
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
        '''
        Параметры: заголовки полей (если ни один заголовок не передан, обрабатываются все заголовки).
        Возвращает список списков,где:
        - первый элемент - список заголовков полей,
        - остальные элементы - списки значений каждого поля.
        '''
        clear_dict = self._clear_dict(*fields)
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
        '''
        Записывает список, переданный в качестве второго позиционного аргумента, в csv-файл с именем, переданным в качестве
        первого позиционного аргумента.
        '''
        with open(name_of_final_file, "w", encoding='utf8') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(list_to_be_written)