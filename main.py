from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re


with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

dict_keys = contacts_list[0]
target_list = []
# pprint(dict_keys)

if __name__ == '__main__':
    # ОЧИЩАЕМ ОТ ПУСТЫХ СТРОК. ОЧИЩЕННЫЕ ДАННЫЕ СКЛАДЫВАЕМ В СЛОВАРЬ
    contacts_list_clean = []  # список данных, очищенных от пустых строк
    count = 0
    for contact_index, contact in enumerate(contacts_list[1:]):
        print(contact_index)
        element_list = []
        for element in contact:
            if element == '':
                continue
            else:
                words = re.split(r'\s', element) # каждое поле записи превращается в список слов
                # print(words)
                element_list.append(words)
        el_dict = dict(zip(dict_keys[0:2], words[0:2]))
        target_list.append(el_dict)
        count += 1
    # pprint(target_list)
        # contacts_list_clean.append(element_list)

    # pprint(contacts_list_clean)

    # ПЫТАЕМСЯ РЕШИТЬ ЗАДАЧУ
    # for contact in contacts_list[1:]:
    #     words = re.findall(r'\w+', str(contact))
    #     # names_list.append(words[0:3])



    # 1. Выполните пункты 1-3 задания.
    # words_pattern = r'\w+'
    # organization_pattern = r'[А-ЯЁа-яё]+'
    # not_name_pattern = r',+'
    # names_list = []
    # not_names_list = []
    # contacts_dict = {'headers': contacts_list[0]}

    # for contact in contacts_list[1:]:
    #     words = re.findall(name_pattern, str(contact))
    #     # names_list.append(words[0:3])
    #     organizations = re.findall(organization_pattern, str(contact))
    #     print(f'words {words}')
    #     print(f'organizations {organizations}')
        # not_names_list.append()
    # contacts_dict['names'] = names_list
    # pprint(contacts_dict)
    # pprint(not_names_list)

    # обрабатываем остальное
    # for
    # for name in names_list:
    #     print(name)


    # если contact[0] не содержит запятых...; если содержит только одну...; если содержит две - ничего не делать




    # re.compile(r'')

    ## 2. Сохраните получившиеся данные в другой файл.
    ## Код для записи файла в формате CSV:
    # with open("phonebook.csv", "w") as f:
    #     datawriter = csv.writer(f, delimiter=',')
    #
    #     ## Вместо contacts_list подставьте свой список:
    #     datawriter.writerows(contacts_list)