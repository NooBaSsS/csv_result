import csv
import os

base = {'id': 0,
        'name': 1,
        'surname': 2,
        'age': 3,
        'height': 4,
        'weight': 5,
        'eyesight': 6,
        'education': 7,
        'english_language': 8,
        }
directory_path = input('Введите путь до ПАПКИ ТОЛЬКО с ФАЙЛАМИ ДЛЯ АНАЛИЗА ' +
                       '(в папке не должно содержаться других .csv файлов): ')
file_extension = '.csv'
candidates = []
sort_idx = []
raw_data = []
sorted_data = []
approved = []


def list_files_in_directory(directory, extension=None):
    '''
    возвращает список .csv файлов, найденых в папке, указанной пользователем
    '''
    absolute_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extension is None or file.endswith(extension):
                absolute_path = os.path.join(root, file)
                absolute_paths.append(absolute_path)
    return absolute_paths


def get_number_of_rows(file_):
    '''
    возвращает количество строк в файле csv
    '''
    with open(file_) as file:
        return len(list(csv.reader(file)))


def get_raw_data(file_):
    '''
    в переменную raw_data записывает каждую строку файла csv в виде списка
    '''
    global raw_data
    raw_data = []
    with open(file_) as file:
        for i in range(get_number_of_rows(file_)):
            reader = csv.reader(file, delimiter='#')
            raw_data.append(next(reader))
    raw_data.pop(0)
    get_sort(file_)


def get_sort(file_):
    '''
    в переменную sort_idx записывает правильный порядок индексов
    '''
    global sort_idx
    sort_idx = []
    with open(file_) as file:
        reader = csv.reader(file, delimiter='#')
        next_row = next(reader)

        right_row_idx = []
        for a in next_row:
            right_row_idx.append(base[a])
        sort_idx = right_row_idx
    sort_data()


def sort_data():
    '''
    сортирует каждый элемент raw_data в по порядку индексов,
    записанных в sort_idx
    '''
    for candidate in raw_data:
        temp_element = {}
        temp_dict = {}
        for i in range(0, 9):
            temp_dict[candidate[i]] = sort_idx[i]
        for element, idx in temp_dict.items():
            temp_element[idx] = element
        sorted_data.append(temp_element)


def qualify():
    '''
    отбрасывает не подходщих кандидатов
    '''
    for candidate in sorted_data:
        if 20 <= int(candidate[3]) or int(candidate[3]) >= 59:
            if 150 <= int(candidate[4]) and int(candidate[4]) <= 190:
                if float(candidate[6]) == 1.0:
                    if candidate[7] == 'Master' or candidate[7] == 'PhD':
                        if candidate[8] == 'true':
                            approved.append(candidate)


def sort_approved():
    '''
    сортрует допущенных в соответствии с правилами
    приоритет от 27 до 37 лет
    далее по алфавиту имя+фамилия
    после сортировки изменяет их id согласно их порядку
    '''
    global approved
    candidates_in_age = []
    candidates_out_age = []
    for candidate in approved:
        if int(candidate[3]) >= 27 and int(candidate[3]) <= 37:
            candidates_in_age.append(candidate)
        else:
            candidates_out_age.append(candidate)
    candidates_in_age = sorted(candidates_in_age, key=lambda d: (d[1], d[2]))
    candidates_out_age = sorted(candidates_out_age, key=lambda d: (d[1], d[2]))
    approved = candidates_in_age + candidates_out_age
    for idx, candidate in enumerate(approved, 1):
        candidate[0] = idx


def write_to_file():
    with open('result.csv', 'w+', newline='') as file:
        writer = csv.writer(file, delimiter='#')
        for element in approved:
            writer.writerow([element[0],
                             element[1],
                             element[2],
                             element[4],
                             element[5],
                             element[7],
                             element[3],
                             ])
        print(f'файл result.csv был сохранен в: {os.path.abspath(file.name)}')


files_list = list_files_in_directory(directory_path, file_extension)
for file_path in files_list:
    print(f'{file_path} в процессе')
    get_raw_data(file_path)
qualify()
sort_approved()
write_to_file()
input('нажмите ENTER для выхода')
