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
# Изменить программу таким образом, чтобы она выгружала данные из CES через базу данных и оптимизировать код.
Skills:
# Разработка Команды для работы с программой.
# Разработка Список данных.
# Администрирование локальных, виртуальных и облачных серверов.
# Разработка Добавление данных в таблице.
# Разработка Добавление данных в файлы.
# Среди новых сайтов, вместо префикса IR используется IO. Добработать программу так, чтобы она считывала данные IO.
# Разработка Кодировка файлов.
# Разработка Анализ данных в базе.
# Разработка Оптимизация кода.
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
Task:
Изменить программу таким образом, чтобы она выгружала данные из CES через базу данных и оптимизировать код.
# Разработка Оптимизация кода.
Decision:
PS C:\Windows\system32> python .\py.py
Список схем баз данных у Ericsson:
Твблица (ces2gErTable, ces4gErTable, ces2gNokTable, ces4gNokTable) с незаполненными данными из CES:
Empty DataFrame
Columns: [BSS, Reg, BS_name, Sector_name]
Index: []
     BSS Reg    BS_name Sector_name
0   None  BU   BU087-B  BU087_014
1   None  BU   BU087-B  BU087_015
2   None  BU   BU087-B  BU087_016
3   None  BU   BU046-B  BU046_014
4   None  BU   BU046-B  BU046_015
5   None  BU   BU046-B  BU046_016
6   None  BU   BU028-B  BU028_021
7   None  BU   BU028-B  BU028_022
8   None  BU   BU028-B  BU028_023
9   None  BU   BU063-B  BU063_021
10  None  BU   BU063-B  BU063_022
11  None  BU   BU063-B  BU063_023
12  None  BU   BU052-B  BU052_014
13  None  BU   BU052-B  BU052_015
14  None  BU   BU052-B  BU052_016
15  None  BU   BU030-B  BU030_021
16  None  BU   BU030-B  BU030_022
17  None  BU   BU030-B  BU030_023
18  None  BU   BU067-B  BU067_021
19  None  BU   BU067-B  BU067_022
20  None  BU   BU067-B  BU067_023
21  None  BU   BU074-B  BU074_014
22  None  BU   BU074-B  BU074_015
23  None  BU   BU074-B  BU074_016
24  None  BU   BU032-B  BU032_021
25  None  BU   BU032-B  BU032_022
26  None  BU   BU032-B  BU032_023
27  None  BU   BU036-B  BU036_021
28  None  BU   BU036-B  BU036_022
29  None  BU   BU036-B  BU036_023
30  None  BU   BU010-B  BU010_031
31  None  BU   BU010-B  BU010_032
32  None  BU   BU010-B  BU010_033
33  None  BU   BU010-B  BU010_034
34  None  BU   BU010-B  BU010_035
35  None  BU   BU010-B  BU010_036
36  None  BU  BU017-BL  BU017_014
37  None  BU  BU017-BL  BU017_015
38  None  BU  BU017-BL  BU017_016
39  None  BU   BU000-B  BU000_021
40  None  BU   BU000-B  BU000_022
41  None  BU   BU000-B  BU000_023
42  None  BU   BU008-B  BU008_031
43  None  BU   BU008-B  BU008_032
44  None  BU   BU008-B  BU008_033
45  None  BU   BU008-B  BU008_034
46  None  BU   BU008-B  BU008_035
47  None  BU   BU008-B  BU008_036
НУЖНО ПРОВЕРИТЬ ДАННЫЕ С NOKIA 2G 4G
    BSS ifBSnameIO ifRegIO Reg BS_number BS_name Sector_name
0  None     HB084      HB  HB      0974  HB084     HB0843
1  None     HB084      HB  HB      0974  HB084     HB0842
2  None     HB084      HB  HB      0974  HB084     HB0841
    BSS ifBSnameIO ifRegIO Reg BS_name Sector_name
0  None     IR011      IR  IR  IR011  IR011_023
1  None     IR011      IR  IR  IR011  IR011_022
2  None     IR011      IR  IR  IR011  IR011_021
ces2gErTable - True
ces4gErTable - False
ces2gNokTable - False
ces4gNokTable - False
Список загруженных файлов в unloading:  ['Er_09122024.xlsx', 'googleEarthData.xlsx', 'N_09122024.xlsx', 'Site_BU00277_1.kml', 'Site_HB00084_6.kml', 'Site_IO00083_1.kml', 'Site_IO00148_1.kml', 'Site_IR00045_1.kml', 'Site_IR00057_1.kml', 'Site_IR00080_1.kml']
...Считываю данные из файла:  Er_09122024.xlsx
...Считываю данные из файла:  googleEarthData.xlsx
...Считываю данные из файла:  N_09122024.xlsx
В файле N_09122024.xlsx данные из еженедельной выгрузки Nokia
...Считываю данные из файла:  Site_BU00277_1.kml
...Считываю данные из файла:  Site_HB00084_6.kml
...Считываю данные из файла:  Site_IO00083_1.kml
...Считываю данные из файла:  Site_IO00148_1.kml
...Считываю данные из файла:  Site_IR00045_1.kml
...Считываю данные из файла:  Site_IR00057_1.kml
...Считываю данные из файла:  Site_IR00080_1.kml
...Считываю данные из файла:  Er_09122024.xlsx
...Считываю данные из файла:  googleEarthData.xlsx
...Считываю данные из файла:  N_09122024.xlsx
В файле N_09122024.xlsx данные из еженедельной выгрузки Nokia
...Считываю данные из файла:  Site_BU00277_1.kml
...Считываю данные из файла:  Site_HB00084_6.kml
...Считываю данные из файла:  Site_IO00083_1.kml
...Считываю данные из файла:  Site_IO00148_1.kml
...Считываю данные из файла:  Site_IR00045_1.kml
...Считываю данные из файла:  Site_IR00057_1.kml
...Считываю данные из файла:  Site_IR00080_1.kml
...Считываю данные из файла:  Er_09122024.xlsx
В файле Er_09122024.xlsx данные из еженедельной выгрузки Ericsson
...Считываю данные из файла:  googleEarthData.xlsx
...Считываю данные из файла:  N_09122024.xlsx
...Считываю данные из файла:  Site_BU00277_1.kml
...Считываю данные из файла:  Site_HB00084_6.kml
...Считываю данные из файла:  Site_IO00083_1.kml
...Считываю данные из файла:  Site_IO00148_1.kml
...Считываю данные из файла:  Site_IR00045_1.kml
...Считываю данные из файла:  Site_IR00057_1.kml
...Считываю данные из файла:  Site_IR00080_1.kml
...Считываю данные из файла:  Er_09122024.xlsx
В файле Er_09122024.xlsx данные из еженедельной выгрузки Ericsson
...Считываю данные из файла:  googleEarthData.xlsx
...Считываю данные из файла:  N_09122024.xlsx
...Считываю данные из файла:  Site_BU00277_1.kml
...Считываю данные из файла:  Site_HB00084_6.kml
...Считываю данные из файла:  Site_IO00083_1.kml
...Считываю данные из файла:  Site_IO00148_1.kml
...Считываю данные из файла:  Site_IR00045_1.kml
...Считываю данные из файла:  Site_IR00057_1.kml
...Считываю данные из файла:  Site_IR00080_1.kml
Таблица (weekly2gNokTable, weekly4gNokTable, weekly2gErTable, weekly4gErTable) из еженедельной выгрузки:
...Считываю данные из файла:  Er_09122024.xlsx
...Считываю данные из файла:  googleEarthData.xlsx
В файле googleEarthData.xlsx данные старых сайтов
...Считываю данные из файла:  N_09122024.xlsx
...Считываю данные из файла:  Site_BU00277_1.kml
...Считываю данные из файла:  Site_HB00084_6.kml
...Считываю данные из файла:  Site_IO00083_1.kml
...Считываю данные из файла:  Site_IO00148_1.kml
...Считываю данные из файла:  Site_IR00045_1.kml
...Считываю данные из файла:  Site_IR00057_1.kml
...Считываю данные из файла:  Site_IR00080_1.kml
...Считываю данные из файла:  Er_09122024.xlsx
...Считываю данные из файла:  googleEarthData.xlsx
...Считываю данные из файла:  N_09122024.xlsx
...Считываю данные из файла:  Site_BU00277_1.kml
В файле Site_BU00277_1.kml данные из сайта RDB
...Считываю данные из файла:  Site_HB00084_6.kml
В файле Site_HB00084_6.kml данные из сайта RDB
...Считываю данные из файла:  Site_IO00083_1.kml
В файле Site_IO00083_1.kml данные из сайта RDB
...Считываю данные из файла:  Site_IO00148_1.kml
В файле Site_IO00148_1.kml данные из сайта RDB
...Считываю данные из файла:  Site_IR00045_1.kml
В файле Site_IR00045_1.kml данные из сайта RDB
...Считываю данные из файла:  Site_IR00057_1.kml
В файле Site_IR00057_1.kml данные из сайта RDB
...Считываю данные из файла:  Site_IR00080_1.kml
В файле Site_IR00080_1.kml данные из сайта RDB
Список доступных команд:  ['Заполненние данных для новых сайтов Nokia (1)', 'Заполненние данных для новых сайтов Ericsson (2)', 'Заполненние данных для довесов Nokia (3)', 'Заполненние данных для довесов Ericsson (4)', 'Объединить таблицы довесов БС с новыми сайтами (5)']
ВНИМАНИЕ! Перед выполнением программы обновите файлы в папке unloading.
Выполните действия: 1
+ Выбрано действие - Заполненние данных для БС Nokia
Можно заполнять новые сайты
Таблица (oldDataTable) из выгрузки Google Earth:
       oldbs reg  latitudeX2  longitudeY2     BSC    LAC
446   IR005  IR   52.25547   104.25783  39402   544
447   IR117  IR   52.28474   104.29864  39402   544
448   IR120  IR   52.31080   104.24059  39402   507
449   IR123  IR   52.21941   104.35359  39402   519
450   IR130  IR   52.27400   104.20639  39402   544
...      ...  ..         ...          ...     ...    ...
2173  SA098  SA   43.91699   145.63936  38453  3002
2174  SA099  SA   43.78800   145.58577  38453  3002
2175  SA011  SA   48.02409   142.17213  38453  3001
2176  SA199  SA   46.96870   142.76949  38453  3000
2177  HB001  HB   48.55849   135.10700     321  3200
[1732 rows x 6 columns]
Таблица (newDataTable) из RDB
  longitudeY1 reg   newbs latitudeX1
1  137.00006  HB  HB084  50.54784
2  103.97092  IO  IO083  52.59574
3  104.04372  IO  IO148  52.40328
4  104.20860  IR  IR045  52.31008
5  103.95059  IR  IR057  52.53094
6  103.83410  IR  IR080  52.48564
Таблица (neighbourTable), соединяющая новые базовые станции с соседними станциями по формуле:
  newbs_x  distance longitudeY1 reg_x newbs_y latitudeX1   oldbs reg_y  latitudeX2  longitudeY2     BSC    LAC
0  HB084  2.728126  137.00006    HB  HB084  50.54784  HB091    HB   48.55849   135.10700     321  3200
1  IO083  0.017160  103.97092    IO  IO083  52.59574  IR103    IR   52.52824   103.96826  40257   572
2  IO148  0.024185  104.04372    IO  IO148  52.40328  IR125    IR   52.46030   104.03698  40257   560
3  IR045  0.008045  104.20860    IR  IR045  52.31008  IR121    IR   52.33974   104.24531  39402   507
4  IR057  0.014709  103.95059    IR  IR057  52.53094  IR132    IR   52.50947   103.98838  40257   591
Source:
# https://stackoverflow.com/questions/57448042/regular-expressions-returning-partial-matches - Регулярные выражения, возвращающие частичные совпадения.
# https://www.w3schools.com/python/ref_string_split.asp - Python String split() Method.
# https://blog.skillfactory.ru/rabota-s-failami-python/ - Чтение файла.
# https://blog.skillfactory.ru/regulyarnye-vyrazheniya-v-python/ - Функции регулярных выражений в Python.
# https://sky.pro/media/zapis-stroki-s-peremennoj-v-tekstovyj-fajl-v-python/ - Запись строки с переменной в текстовый файл в Python.
# https://sky.pro/wiki/python/dobavlyaem-novuyu-stroku-pri-zapisi-v-fayl-python-file-write/ - Добавляем новую строку при записи в файл Python: file.write().
# https://pythonru.com/primery/kak-perevesti-tekst-na-novuju-stroku-v-python - Символ новой строки в print.
# https://timeweb.cloud/tutorials/python/kak-udalit-simvol-iz-stroki-python - Как удалить символы с помощью среза.
# https://www.w3schools.com/python/python_while_loops.asp - The break Statement.
# https://sky.pro/wiki/python/kak-dobavit-element-v-spisok-v-python/ - Использование метода append() для добавления элемента.
# https://pythonist.ru/kak-dobavit-element-v-slovar/ - Совет: добавление и обновление происходит одинаково.
# https://ru.stackoverflow.com/questions/1599918/%d0%9a%d0%b0%d0%ba-%d0%bc%d0%bd%d0%b5-%d0%b2-%d0%b3%d0%be%d1%82%d0%be%d0%b2%d1%8b%d0%b9-%d1%81%d0%bb%d0%be%d0%b2%d0%b0%d1%80%d1%8c-%d0%b4%d0%be%d0%b1%d0%b0%d0%b2%d0%b8%d1%82%d1%8c-%d0%ba%d0%bb%d1%8e%d1%87%d0%b8-%d0%b8-%d0%b7%d0%bd%d0%b0%d1%87%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b8%d0%b7-%d0%b4%d0%b2%d1%83%d1%85-%d1%81%d0%bf%d0%b8%d1%81%d0%ba%d0%be%d0%b2/1599920#1599920 - Как мне в готовый словарь добавить ключи и значения из двух списков?
# https://stepik.org/lesson/265110/step/2?unit=246058 - Евклидово расстояние.
# https://habr.com/ru/articles/801885/ - Принцип работы KNN.
# https://sky.pro/media/poluchenie-indeksa-maksimalnogo-ili-minimalnogo-znacheniya-v-spiske-v-python/ - Использование встроенных функций max(), min() и index().
# https://stackoverflow.com/questions/27749553/how-can-i-read-the-contents-of-all-the-files-in-a-directory-with-pandas - How can I read the contents of all the files in a directory with pandas?
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html - Как объединить две таблицы в pandas?
# https://sky.pro/wiki/python/udalenie-dublikatov-v-pandas-data-frame-po-vybrannym-kolonkam/ - Удаление дубликатов в Pandas DataFrame по выбранным колонкам.
# https://world-hello.ru/python/pandas/pandas-osnovnye-obekty-dataframe.html - Конвертирование словаря в Pandas DataFrame.
# https://sky.pro/media/kak-preobrazovat-indeks-dataframe-v-stolbecz-v-pandas/ - Как преобразовать индекс DataFrame в столбец в Pandas.
# https://ru.stackoverflow.com/questions/1486105/%D0%9F%D0%BE%D0%BC%D0%BE%D0%B3%D0%B8%D1%82%D0%B5-%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D1%83%D0%B9%D1%81%D1%82%D0%B0-%D1%81%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C-%D0%BE%D0%B4%D0%B8%D0%BD-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%B2%D1%81%D0%B5%D1%85-%D0%B8%D0%BC%D1%91%D0%BD-%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2-%D0%B8%D0%B7-%D0%BF%D0%B0%D0%BF%D0%BA%D0%B8 - Помогите пожалуйста сделать один список всех имён файлов из папки.
# https://sky.pro/media/udalenie-dublikatov-iz-spiska-v-python-sohranyaya-poryadok/ - Удаление дубликатов из списка в Python, сохраняя порядок.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html - pandas.DataFrame.merge.
# https://www.geeksforgeeks.org/how-to-convert-strings-to-floats-in-pandas-dataframe/ - Convert String to Float in DataFrame Using DataFrame.astype().
# https://ru.stackoverflow.com/questions/1601516/%d0%9a%d0%b0%d0%ba-%d1%80%d0%b5%d1%88%d0%b8%d1%82%d1%8c-%d0%bf%d1%80%d0%be%d0%b1%d0%bb%d0%b5%d0%bc%d1%83-%d1%81-typeerror-cannot-convert-the-series-to-class-float - Как решить проблему с TypeError: cannot convert the series to <class 'float'>?
# https://nerdit.ru/pandas-groupby/ - Исследование группировки данных с помощью Pandas GroupBy.
# https://sky.pro/media/konvertacziya-vyvoda-groupby-iz-series-v-dataframe-v-pandas/ - Конвертация вывода GroupBy из Series в DataFrame в Pandas.
# https://docs-python.ru/packages/modul-pandas-analiz-dannykh-python/duplicates-drop-duplicates/#:~:text=%D0%9F%D0%BE%20%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E%2C%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%20%D1%83%D0%B4%D0%B0%D0%BB%D1%8F%D0%B5%D1%82%20%D0%BF%D0%BE%D0%B2%D1%82%D0%BE%D1%80%D1%8F%D1%8E%D1%89%D0%B8%D0%B5%D1%81%D1%8F%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8%20%D0%BD%D0%B0%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%B5%20%D0%B2%D1%81%D0%B5%D1%85%20%D1%81%D1%82%D0%BE%D0%BB%D0%B1%D1%86%D0%BE%D0%B2.&text=%D0%A7%D1%82%D0%BE%D0%B1%D1%8B%20%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C%20%D0%B4%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%82%D1%8B%20%D0%B2%20%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D1%82%D0%BE%D0%BB%D0%B1%D1%86%D0%B0%D1%85%2C%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D0%BC%20%D0%B0%D1%80%D0%B3%D1%83%D0%BC%D0%B5%D0%BD%D1%82%20subset%20.&text=%D0%A7%D1%82%D0%BE%D0%B1%D1%8B%20%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C%20%D0%B4%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%82%D1%8B%20%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D1%81%D1%82%D0%BE%D0%BB%D0%B1%D1%86%D0%BE%D0%B2,%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%B8%D0%B5%20%D0%B2%D1%85%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F%2C%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D0%BC%20%D0%B0%D1%80%D0%B3%D1%83%D0%BC%D0%B5%D0%BD%D1%82%20keep%20. - Пример использования DataFrame.drop_duplicates().
# https://pythonru.com/osnovy/python-dict?ysclid=m4i4x8fzy6280189267 - Создание словаря.
# https://yandex.ru/search/?text=pandas+%D0%BF%D0%BE%D0%BC%D0%B5%D0%BD%D1%8F%D1%82%D1%8C+%D0%BC%D0%B5%D1%81%D1%82%D0%B0%D0%BC%D0%B8+%D1%81%D1%82%D0%BE%D0%BB%D0%B1%D1%86%D1%8B&clid=2411726&lr=65 - pandas поменять местами столбцы.
# https://yandex.ru/search/?text=python+%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0+%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB%D0%BE%D0%B2+%D0%B2+%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B5&clid=2411726&lr=65 - python замена символов в строке.
# https://ru.stackoverflow.com/questions/700664/%D0%A3%D0%B7%D0%BD%D0%B0%D1%82%D1%8C-%D0%BA%D0%BE%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D1%83-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0 - Узнать кодировку файла.
# https://pythonist.ru/konstrukcziya-match-case-v-python-polnoe-rukovodstvo/?ysclid=m4t5mkumhv16549810 - Конструкция match-case в Python.
# https://sky.pro/media/proverka-na-pustotu-dataframe-v-pandas/#:~:text=%D0%9A%D0%B0%D0%BA%20%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%2C%20%D0%BF%D1%83%D1%81%D1%82%D0%BE%D0%B9%20%D0%BB%D0%B8%20DataFrame,%D0%B8%20False%20%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D0%BC%20%D1%81%D0%BB%D1%83%D1%87%D0%B0%D0%B5.&text=%D0%A2%D0%B0%D0%BA%D0%B8%D0%BC%20%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%BC%2C%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B8%20DataFrame%20%D0%BD%D0%B0%20%D0%BF%D1%83%D1%81%D1%82%D0%BE%D1%82%D1%83%20%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D1%82%D0%BE%D1%87%D0%BD%D0%BE%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%20empty%20. - Проверка на пустоту DataFrame в pandas.
# https://stackoverflow.com/questions/44893565/get-list-of-mysql-databases-with-python - Get list of MySQL databases with python.
# https://www.geeksforgeeks.org/how-to-find-tables-that-contain-a-specific-column-in-sql-using-python/ - How to find tables that contain a specific column in SQL using Python?
# https://sky.pro/media/podklyuchenie-k-baze-dannyh-mysql-s-pomoshhyu-python/ - Операции с данными.
# https://translated.turbopages.org/proxy_u/en-ru.ru.c689cc14-676ba6bc-ea87ebc9-74722d776562/https/www.geeksforgeeks.org/creating-a-pandas-dataframe-using-list-of-tuples/ - С помощью функции pd.DataFrame().
# https://translated.turbopages.org/proxy_u/en-ru.ru.3168aa15-676bbc3e-792382c9-74722d776562/https/www.geeksforgeeks.org/ways-to-filter-pandas-dataframe-by-column-values/ - Фильтровать фрейм данных Pandas по значению столбца.
# https://stackoverflow.com/questions/12065885/filter-dataframe-rows-if-value-in-column-is-in-a-set-list-of-values - Filter dataframe rows if value in column is in a set list of values [duplicate].
# https://stackoverflow.com/questions/3783238/python-database-connection-close - Python Database connection Close.
# https://translated.turbopages.org/proxy_u/en-ru.ru.2cd2a668-676d034b-7548ed9e-74722d776562/https/stackoverflow.com/questions/59442258/effecient-way-to-repeat-y-n-question-in-python - Эффективный способ повторить y / n вопрос в python [дублировать].
# https://yandex.ru/search/?text=python+%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B8%D1%82%D1%8C+%D0%B8%D0%BB%D0%B8+%D0%BD%D0%B5%D1%82+y%2Fn&lr=65&clid=2411726 - python продолжить или нет y/n.
# https://tonais.ru/library/dobavlenie-i-udalenie-stolbtsa-v-dataframe#:~:text=%D0%A7%D1%82%D0%BE%D0%B1%D1%8B%20%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C%20%D0%B8%D0%BB%D0%B8%20%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE,Pandas%2C%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B9%D1%82%D0%B5%20%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D1%8E%20drop%20() - Пример 4: с помощью функции drop().