Цель:
# Перечислить список команд, которые может выполнить программа.
# Собрать в список данные, которые необходимо заполнить в шаблоне.
# Настроить библиотеку для работы с таблицами excel.
# Найти незаполненные строки БС в таблице из CES для каждых технологий - 2g, 4g.
# Добавить имееющиеся данные в таблице из еженедельной выгрузки.
# Добавить данные координат в таблицу из rdb.
# Добавить данные LAC и BSC в таблицу и в пустой словарь название БС, координаты, LAC И BSC.
# Найти ближайшего соседа базовой станции по формуле sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)).
# Объединить таблицы с довесами и новыми базовыми станциями.
# Добавить файл csv данные, полученные из таблиц.
# Замена строк в таблицах.
# Добработать программу так, чтобы она считывала данные IO.
# Узнать кодировку файла.
# Добавить аналогичным образом данные для технологий Ericsson.
# Подключиться к базе.
# В какой базе находится таблица LNHOIF.
# Найти в какой таблице и базе находятся незаполненные данные из CES.
# Найти незаполненные данные 2g, 4g из CES в базе данных.
# Написать отдельную программу, для выгрузки координат, контроллеров и Lac старых сайтов.
Skills:
# Разработка Команды для работы с программой.
# Разработка Список данных.
# Администрирование локальных, виртуальных и облачных серверов.
# Разработка Добавление данных в таблице.
# Разработка Добавление данных в файлы.
# Среди новых сайтов, вместо префикса IR используется IO. Добработать программу так, чтобы она считывала данные IO.
# Разработка Кодировка файлов.
# Разработка Анализ данных в базе.
Task:
Настроить библиотеку для работы с таблицами excel.
# Администрирование локальных, виртуальных и облачных серверов.
Decision:
PS C:\Windows\system32> pip install pandas --proxy http://tdomain-fgproxy.corp.tdomain.ru:8080
root@kvmubuntu:~# python -m venv sortenv
root@kvmubuntu:~# source sortenv/Scripts/activate
root@kvmubuntu:~# touch requirements.txt
root@kvmubuntu:~# cat requirements.txt
pandas==2.2.3
openpyxl==3.1.5 
root@kvmubuntu:~# pip install -r requirements.txt
Task:
Заполнить данные для новых сайтов Nokia.
# Разработка Добавление данных в таблице.
Decision:
PS C:\Windows\system32> python3 .\dataNokia.py
['Заполненние данных для БС Nokia (1)', 'Заполненние данных для БС Ericsson (2)']
ВНИМАНИЕ! Перед выполнением программы добавьте файлы в папку unloading.
Выполните действия: 1
Для заполнения нужны следующие данные:  ['Reg', 'CELL', 'SW', 'BSC', 'BCF', 'LAC', 'RAC2g', 'Имя сайта', 'RAC3g', 'URA', 'RNC_ID']
Список загруженных файлов в unloading:  ['N_09122024.xlsx', 'Site_IO00019_2.kml', 'Table integrated sites (2).xlsx', 'Table integrated sites (3).xlsx']
... Корректировка префикса:
IO019
IO
IR019
IR
Таблицы (allBs2gTable, allBs4gTable) с довесами и новыми базовыми станциями 2g, 4g:
  Reg     CELL    SW  Values  BS_number  locationAreaIdLAC  rac
0  IR  IO0191  MR10  IRK84        19               528   8
1  IR  IO0192  MR10  IRK84        19               528   8
2  IR  IO0193  MR10  IRK84        19               528   8
   Reg Имя системного модуля Sector_name   tac
0   IR                IO019  IO019_016  528
2   IR                IO019  IO019_015  528
4   IR                IO019  IO019_014  528
6   IR                IO019  IO019_083  528
8   IR                IO019  IO019_082  528
10  IR                IO019  IO019_081  528
Do you want to continue? (y/n): n
Task:
При загрузке файлов на сайт, столкулся с проблемой, что файлы не грузятся из-за неправильного формата. Есть шаблонный файл, у которой правильная кодировка. Можно сравнить два файла, написав программу, которая определяет кодировку файлов.
# Разработка Кодировка файлов.
Decision:
PS C:\Windows\system32> pip install chardet  --proxy http://tdomain-fgproxy.corp.tdomain.ru:8080
PS C:\Windows\system32> python .\encoding.py
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
PS C:\Windows\system32> python .\encoding.py
{'encoding': 'UTF-8-SIG', 'confidence': 1.0, 'language': ''}
Task:
Найти незаполненные данные 2g, 4g из CES в базе данных.
# Разработка Анализ данных в базе.
Decision:
PS C:\Windows\system32> python .\querryManager.py
['Показать список баз (1)', 'В какой базе находится определенная таблица (2)', 'Найти строки во всей базе, в которой есть определенная имя базовая станции (3)', 'Найти строки в одной базе, в которой есть определенная имя базовая станции (4)', 'Выборка (5)']
Выполните действия от 1 до : 5
Выберите базу: tdb
Выберите столбцы: *
Выберите таблицу: table_ericsson_2g_v
Выберите условие: WHERE Reg='VV' AND BSS IS NULL ORDER BY Date DESC LIMIT 5
(73459, datetime.datetime(2024, 12, 24, 10, 59, 53), None, None, None, 'OK', 'VV', '-', 'VV455-B', 'true', '-', '-', None, None, 'VV2551', '0522', None, None, 'Край Приморский, Город Уссурийск, Улица, Дом 67', None, None, None, 'Radio22xx', 'AB', 'false', 'BB Port A', '6630', 'GSM1800', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'TN_C', 'BB/TN_C/copper')
Взято из Базы: tdb Таблицы: table_ericsson_2g_v
(73460, datetime.datetime(2024, 12, 24, 10, 59, 53), None, None, None, 'OK', 'VV', '-', 'VV455-B', 'true', '-', '-', None, None, 'VV2552', '0522', None, None, 'Край Приморский, Город Уссурийск, Улица, Дом 67', None, None, None, 'Radio22xx', 'AB', 'false', 'BB Port B', '6630', 'GSM1800', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'TN_C', 'BB/TN_C/copper')
Взято из Базы: tdb Таблицы: table_ericsson_2g_v
(73461, datetime.datetime(2024, 12, 24, 10, 59, 53), None, None, None, 'OK', 'VV', '-', 'VV255-B', 'true', '-', '-', None, None, 'VV2553', '0522', None, None, 'Край Приморский, Город Уссурийск, Улица, Дом 67', None, None, None, 'Radio22xx', 'AB', 'false', 'BB Port C', '6630', 'GSM1800', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'TN_C', 'BB/TN_C/copper')
Взято из Базы: tdb Таблицы: table_ericsson_2g_v
Do you want to continue? (y/n): n
