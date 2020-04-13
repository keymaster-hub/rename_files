import os



def exchange():
    """
    Возвращает список имен .tif файлов для которых есть - имя-ЗАМЕНА
    """
    exchange = []
    for name in os.listdir():
        if 'ЗАМЕНА' in name and ''.join(name.split())[:-11]+'.tif' in os.listdir():
            exchange.append(''.join(name.split())[:-11]+'.tif')
    return exchange        

def ask_user():
    print(*exchange())
    check = str(input('Delete files? Y/N:\n')).lower().strip()
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



def find_wrong_names():
    """
    Возвращает список *.tif файлов в текущей папке
    не проходящих по маске А123456*.tif
    """
    files_list = os.listdir()
    tif_list = []
    wrong_list = []
    pos = 0
    #Создаем список *.tif файлов
    for i in files_list:
        if str(i)[-4:] == str('.tif'):
            tif_list.insert(pos, i)
            pos += 1
    pos = 0
    #Создаем список файлов где после 1 символа меньше 6 цифр или 1 символ lower case
    for i in tif_list:
        if (str(i)[1:7]).isdigit() is False: #Меньше 6 цифр - в список
            wrong_list.insert(pos, i)
        elif (str(i)[0]).isupper() is False: #1 символ нижний регистр - в список
            wrong_list.insert(pos, i)
    return wrong_list


def rename_files():
    """
    Предлагает вариант переименования
    """
    wrong_list = find_wrong_names()
    wrong_list_1=[] #Список с именами на "Э" куда добавить единицы
    wrong_list_0=[] #Список с остальными именами куда добавить нули
    
    for i in wrong_list:
        if str(i[0]).lower() == str('э'):
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

    return wrong_list_1 + wrong_list_0

def ask_user():
    check = str(input('Rename? Y/N:\n')).lower().strip()
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
input('Press ENTER to exit')
