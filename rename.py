import os
import pandas
import shutil

"""
/
/
/
Функции которые мне не хочется выносить в отдельный файл, потому что их
не так много.
/
/
/
"""


def tif_files_list():
    """
    Возвращает список .tif файлов в текущей директории
    """
    tif_list = []
    files_list = os.listdir()
    for name in files_list:
        if str(name)[-4:] == str('.tif'):
            tif_list.append(name)
    return(tif_list)        


def find_spaces():
    """
    Возвращает список файлов с пробелами или _ в имени или англ "с"
    В виде списка [НЕпраильное имя1, правильное имя1, ...]
    """
    wrong_names = []
    for i in tif_files_list():
        if ' ' in str(i):
            wrong_names.append(i)
            wrong_names.append(''.join(i.split()))
        elif '_' in str(i):
            wrong_names.append(i)
            wrong_names.append(i.replace('_', '-'))
        elif 'c' in str(i):
            wrong_names.append(i)
            wrong_names.append(i.replace('c', 'с'))
    return(wrong_names)

def ask_user():
    """
    Стандартная функция для подтверждения от пользователя
    Возвращает True если 'y' или False если 'n'
    """
    check = str(input('Rename files? Y/N:\n')).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()


def remove_spaces():
    """
    Удаляет пробелы и _ в именах файлов
    """
    rename_list = find_spaces()
    for i in range(0, len(rename_list), 2):
        print(str(rename_list[i]), '-->', str(rename_list[i+1]))               
    if len(rename_list):   #Проверка не пустой ли список => все имена корректны            
        if ask_user():
            for i in range(0, len(rename_list), 2):
                os.rename(rename_list[i], rename_list[i+1])
                print(rename_list[i], ' is renamed to - ', rename_list[i+1])
            print('Done!')
        else:
            print('Break')
    else:
        print('Nothing with spaces or _')
            
    
def exchange():
    """
    Возвращает список имен файлов для которых есть - 'ЗАМЕНА'
    """
    exchange = []
    for name in tif_files_list():
        if 'ЗАМЕНА' in name.upper() and ''.join(name.split())[:-11]+'.tif' in os.listdir():
            exchange.append(''.join(name.split())[:-11]+'.tif')
    return exchange        


def find_wrong_names():
    """
    Возвращает список *.tif файлов в текущей папке
    не проходящих по маске А123456*.tif
    """
    tif_list = tif_files_list()
    wrong_names = []
    #Создаем список файлов где после 1 символа меньше 6 цифр или 1 символ lower case
    for i in tif_list:
        if (str(i)[1:7]).isdigit() is False: #Меньше 6 цифр - в список
            wrong_names.insert(pos, i)
        elif (str(i)[0]).isupper() is False: #1 символ нижний регистр - в список
            wrong_names.append(i)
    return wrong_names


def rename_files():
    """
    Предлагает вариант переименования
    """
    wrong_list = find_wrong_names()
    wrong_list_1=[] #Список с именами на "Э" куда добавить единицы
    wrong_list_0=[] #Список с остальными именами куда добавить нули
    wrong_list_spaces=[] #Список с пробелами и _ нижним подчеркиванием
    for i in wrong_list:
        if ' ' in str(i): #Если есть пробелы в имени
            wrong_list_spaces.append(i)
            wrong_list_spaces.append(''.join(i.split()))
        elif '_' in str(i):
            wrong_list_spaces.append(i)
            wrong_list_spaces.append(i.replace('_', '-'))
        elif str(i[0]).lower() == str('э'):
            num_count = 0
            for x in str(i)[1:]:
                if x.isdigit():
                    num_count += 1
                else:
                    break
            paste = 6 - num_count        #Сколько единиц вставить
            paste_str = str('1') * paste #Строка из единиц
            wrong_list_1.append(i)       #Добавляем старое имя файла
            wrong_list_1.append(str(i[0]).upper()+str(paste_str)+str(i[1:]))#Добавляем новое имя

        else:
            num_count = 0
            for x in str(i)[1:]:
                if x.isdigit():
                    num_count += 1
                else:
                    break
            paste = 6 - num_count        #Сколько нулей вставить
            paste_str = str('0') * paste #Строка из нулей
            wrong_list_0.append(i)       #Добавляем старое имя файла
            wrong_list_0.append(str(i[0]).upper()+str(paste_str)+str(i[1:]))#Добавляем новое имя    
    return wrong_list_1 + wrong_list_0 + wrong_list_spaces


def ask_user_del():
    for name in exchange():
        print(name)
    check = str(input('delete files? Y/N:\n')).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()


def excel_search():
    """
    Возвращает список имен файлов которые есть в экселе
    """
    move_list = []
    excel_data = pandas.read_excel('X:\_\Отчет 2020.xlsx', sheet_name = 'Принято')
    excel_list = excel_data.to_csv(index=False)
    for name in tif_files_list():
        if name[:1].lower() + name[1:-4].replace('-', '/') in excel_list:
            move_list.append(name)
    return move_list


    
"""
/
/
/
-------------------------------------Программа----------------------------------------------
/
/
/
"""


remove_spaces()    #Убираем пробелы и _

if exchange():
    if ask_user_del():
        for file in exchange():
            os.remove(file)
            print('file', file, 'deleted')
else:
    print('Nothing to delete')

rename_list = rename_files()
for i in range(0, len(rename_list), 2):
    print(str(rename_list[i]), '-->', str(rename_list[i+1]))               
if len(rename_list):   #Проверка не пустой ли список => все имена корректны            
    if ask_user():
        for i in range(0, len(rename_list), 2):
            os.rename(rename_list[i], rename_list[i+1])
            print(rename_list[i], ' is renamed to - ', rename_list[i+1])
        print('Done!')
    else:
        print('Break')
else:
    print('Nothing to rename')
    
move_list = excel_search()
if len(move_list):
    print('Переместить файлы:')
    for i in move_list:
        print(i)
    print('В папку "Готовые"?')
    if ask_user():
        for i in move_list:
            shutil.move(i, ('D:\Почта\Работа\Готовые\\' + i))
            print(i + ' successfuly moved')
            

input('Press ENTER to exit')
