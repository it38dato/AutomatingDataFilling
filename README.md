Цель:
# Перечислить список команд, которые может выполнить программа.
# Собрать в список данные, которые необходимо заполнить в шаблоне.
# Настроить библиотеку для работы с таблицами excel.
# Найти незаполненные строки БС в таблице из CES для каждых технологий - 2g, 4g.
Skills:
# Разработка Команды для работы с программой.
# Разработка Список данных.
# Администрирование локальных, виртуальных и облачных серверов.
# Разработка Поиск незаполненных данных в таблице.
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