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
Skills:
# Разработка Команды для работы с программой.
# Разработка Список данных.
# Администрирование локальных, виртуальных и облачных серверов.
# Разработка Добавление данных в таблице.
# Разработка Добавление данных в файлы.
# Среди новых сайтов, вместо префикса IR используется IO. Добработать программу так, чтобы она считывала данные IO.
# Разработка Кодировка файлов.
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
IO0129
IO
IR0129
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