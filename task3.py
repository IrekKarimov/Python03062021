"""
Задача 3
Напишите прототип тестовой системы, состоящей из двух тест-кейсов.
 В данной задаче использование стороннего модуля для автоматизации тестирования не приветствуется.
Тестовая система представляет собой иерархию классов, описывающую тест-кейсы.
У каждого тест-кейса есть:
•	Номер (tc_id) и название (name)
•	Методы для подготовки (prep), выполнения (run) и завершения (clean_up) тестов.
•	Метод execute, который задаёт общий порядок выполнения тест-кейса и обрабатывает исключительные ситуации.
Все этапы выполнения тест-кейса, а также исключительные ситуации должны быть задокументированы в лог-файле или в стандартном выводе.
Тест-кейс 1: Список файлов
•	[prep] Если текущее системное время, заданное как целое количество секунд от начала эпохи Unix, не кратно двум,
 то необходимо прервать выполнение тест-кейса.
•	[run] Вывести список файлов из домашней директории текущего пользователя.
•	[clean_up] Действий не требуется.
Тест-кейс 2: Случайный файл
•	[prep] Если объем оперативной памяти машины, на которой исполняется тест, меньше одного гигабайта,
 то необходимо прервать выполнение тест-кейса.
•	[run] Создать файл test размером 1024 КБ со случайным содержимым.
•	[clean_up] Удалить файл test.

"""
import unittest
import time
from pathlib import Path
import os
import random
#import psutil



# Базовый класс для TestCase
class BaseTestCase:
    log_file = '.\log.txt'
    def __init__(self, tc_id, name):
         self.tc_id = tc_id
         self.name = name



# Класс TestCase_1
class TestCase_1(BaseTestCase):
    num_files = 0
    def prep(self):
        t = int(time.time())
        # Возвращаем True, если время четное, иначе False
        return t % 2 == 0

    def run(self):
        # Получение и воврат списка файлов в домашней директории текущего пользователя
        home_folder = Path.home()
        files = os.listdir(home_folder)
        return [str(home_folder), files, len(files)]

    def execute(self):
        # Открываем файл в режиме записи для лога
        f = open(self.log_file, 'w')
        f.writelines('Execute TestCase tc_id = ' + str(self.tc_id) + ' name = ' + self.name + '\n')

        # Порядок запуска функций
        t = self.prep()
        if t:
            res = self.run()
            self.num_files = res[2]
            if res[0]:
                # Запись списка файлов в лог
                f.writelines('Files in Home directory ' + str(res[0]) + ': ' + str(res[2]) + '\n')
                for s in res[1]:
                    f.writelines(s + '\n')
        else:
            f.writelines('Interrupt of TestCase ' + self.name + '\n')
            if f:
                f.close()
            return

        if self.clean_up():
            f.writelines('End of TestCase ' + self.name + '\n')

        if f:
            f.close()

    def clean_up(self):
        return True


# Класс TestCase_2
class TestCase_2(BaseTestCase):
    ram_size = 0
    test_file = '.\\test'
    def prep(self):
        #print(psutil.virtual_memory())
        # Заглушка. Возвращаем размер ОЗУ
        return 1073741825

    def run(self):
        one_mb = 1048576
        # Создаем файл test в текущей директории
        try:
            f = open(self.test_file, 'wb')
            # Заполняем случайными символами
            while os.path.getsize(self.test_file) < one_mb:
                s = random.randint(1, 256)
                f.write(chr(s).encode('utf-8'))
        except IOError:
            # Системная ошибка при открытии файла
            return False
        if f:
            f.close()
        return True

    def clean_up(self):
        try:
            if os.path.exists(self.test_file):
                pass
                os.remove(self.test_file)
        except IOError:
            # Системная ошибка при удалении файла
            return False
        return True

    def execute(self):
        one_gb = 1073741824
        # Открываем файл в режиме записи для лога
        f = open(self.log_file, 'a')
        f.writelines('\nExecute TestCase tc_id = ' + str(self.tc_id) + ' name = ' + self.name + '\n')

        # Порядок запуска функций
        self.ram_size = self.prep()
        if self.ram_size > one_gb:
            # Если ОЗУ больше 1Гб
            res = self.run()
        else:
            # Иначе прерываем
            f.writelines('Interrupt of TestCase ' + self.name + '\n')
            if f:
                f.close()
            return

        if self.clean_up():
            f.writelines('End of TestCase ' + self.name + '\n')
        else:
            f.writelines('Error create or remove file ' + self.test_file + '\n')

        if f:
            f.close()




# Unittest for TestCase
class TestCase(unittest.TestCase):

    # Тест для сласса TestCase_1
    def test_TestCase_1(self):
        # Создаем и запускаем экземпляр класса TestCase_1
        tc1 = TestCase_1(123, 'TestCase_1')
        tc1.execute()

        # Получение количества файлов в домашней директории текущего пользователя
        home_folder = Path.home()
        num_files = len(os.listdir(home_folder))
        print('\nTesting class: ' + tc1.name + ', tc_id: ' + str(tc1.tc_id) + '\n')
        self.assertEqual(tc1.num_files, num_files)

    # Тест для сласса TestCase_2
    def test_TestCase_2(self):
        # Создаем и запускаем экземпляр класса TestCase_2
        tc2 = TestCase_2(456, 'TestCase_2')
        print('\nTesting class: ' + tc2.name + ', tc_id: ' + str(tc2.tc_id) + '\n')
        tc2.execute()
        ram_size = 1073741825
        self.assertEqual(tc2.ram_size, ram_size)

        fe = os.path.exists(tc2.test_file)
        self.assertEqual(fe, False)


if __name__ == '__main__':
    unittest.main()
