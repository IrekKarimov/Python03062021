"""
Задача 1
Реализовать программу, осуществляющую копирование файлов в соответствии с конфигурационным файлом.
Конфигурационный файл должен иметь формат xml.
Для каждого файла в конфигурационном файле должно быть указано его имя,
исходный путь и путь, по которому файл требуется скопировать.

Пример
Конфигурационный файл:

<config>
    <file
            source_path="C:\Windows\system32"
            destination_path="C:\Program files"
            file_name="kernel32.dll"
    />
    <file
            source_path="/var/log"
            destination_path="/etc"
            file_name="server.log"
    />
</config>
"""

import xml.etree.ElementTree as ET
import os.path
import shutil

# XML файл конфиги
conf_fname = ".\conf.xml"

# Файл для логирования
log_file = ".\log.txt"

# Открываем файл для записи лога
f_log = open(log_file, 'w')

# Читаем XML файл
root_node = ET.parse(conf_fname).getroot()

# Проходим по XML дереву с именем <file>
for tag in root_node.findall('file'):
    # Считываем атрибуты
    file_name = tag.get('file_name')
    source_file = tag.get('source_path') + '\\' + file_name
    destination_file = tag.get('destination_path') + '\\' + file_name

    if os.path.exists(source_file):
        # Если файл-источник существует, копируем
        try:
            shutil.copy(source_file, destination_file)
        except (IOError, Exception) as e:
            # Пишем в лог системную ошибку
            f_log.write(str(e) + '\n')

        if os.path.exists(destination_file):
            # Если копирование успешно
            # Запись лога
            f_log.write('File <' + source_file + '> copied in <' + destination_file + '>' + '\n')
        else:
            # Если файл не скопировался
            f_log.write('Error copy file to ' + destination_file + ' from ' + source_file + '\n')

    else:
        # Если файл-источник не найден пишем в логе ошибку
        f_log.write('File ' + source_file + ' not found' + '\n')


f_log.close()


