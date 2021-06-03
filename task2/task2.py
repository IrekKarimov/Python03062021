""""
Задача 2
 Дан файл, содержащий имена файлов, алгоритм хэширования (один из MD5/SHA1/SHA256) и соответствующие им хэш-суммы,
 вычисленные по соответствующему алгоритму и указанные в файле через пробел.
 Напишите программу, читающую данный файл и проверяющую целостность файлов.

Пример
Файл сумм:
file_01.bin md5 aaeab83fcc93cd3ab003fa8bfd8d8906
file_02.bin md5 6dc2d05c8374293fe20bc4c22c236e2e
file_03.bin md5 6dc2d05c8374293fe20bc4c22c236e2e
file_04.txt sha1 da39a3ee5e6b4b0d3255bfef95601890afd80709
Пример вызова:
<your program> <path to the input file> <path to the directory containing the files to check>
Формат вывода:
file_01.bin OK
file_02.bin FAIL
file_03.bin NOT FOUND
file_04.txt OK

"""

import hashlib
import sys


def Check_Hash(file, hash_method, hash):
    """"
     Функция Check_Hash(file, hash_method, hash) вычисляет хэш файла 'file' по методу 'hash_method' и
     сравнивает с хэшем 'hash'.
     Возвращает 1 если хэши совпали, иначе 0, -1 если системная ошибка
    """
    f_hash = ''

    try:
        # Открываем файл в режиме чтения для вычисления хэша
        f = open(file, 'rb')
        readfile = f.read()
        if hash_method == 'md5':
            f_hash = hashlib.md5(readfile)
        elif hash_method == 'sha1':
            f_hash = hashlib.sha1(readfile)
        elif hash_method == 'sha256':
            f_hash = hashlib.sha256(readfile)
    except (IOError, Exception) as e:
        # Системная ошибка при открытии файла
        return -1

    f.close()
    f_hash = f_hash.hexdigest()

    return f_hash == hash



# Файл со списком
f_name = '.\hash.txt'

# Каталог файлов
dir_name = '.\\source'

# Если есть аргументы в коммандной строке
if len(sys.argv) > 1:
    f_name = sys.argv[1]
    dir_name = sys.argv[2]

# Файл для лога
log_file = open('.\log.txt', 'w')

try:
    f = open(f_name)
    # Читаем построчно файл со списком
    for s in f.readlines():
        # Разбиваем строку по пробелам
        a = s.split(' ')
        # Удаляем символ перевод строки
        f_hash = a[2][:-1]
        result = Check_Hash(dir_name + '\\' + a[0], a[1].lower(), f_hash.lower())
        if result == 1:
            log_file.writelines(a[0] + ' OK\n')
        elif result == 0:
            log_file.writelines(a[0] + ' FAIL\n')
        elif result < 0:
            log_file.writelines(a[0] + ' NOT FOUND\n')

except (IOError, Exception) as e:
    print(str(e) + '\n')

f.close()
log_file.close()
