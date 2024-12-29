import mysql.connector
import sys
repeat="y"
with open("output.log", "w") as outfile:
    outfile.write("") 
while repeat == "y":
    print("Выполните действия от 1 до 2:")
    listcmd=['Показать список баз (1)', 'В какой базе находится определенная таблица (2)', 'Найти таблицу в базе по определенным столбцам (3)' ]
    print(listcmd)
    choicecmd = input()
    #print(choicecmd)
    if choicecmd == '1':
        with open("output.log", "a") as outfile:
                outfile.write("... Подключаюсь к БД."+"\n")
        try: 
            mydb = mysql.connector.connect(
                host="ip_nokia",
                user="tuser",
                password="tpassword",
            )
            with open("output.log", "a") as outfile:
                    outfile.write("+ Успешное подключение к БД."+"\n")
        except mysqldb.Error as e: 
            print(f"Error connecting to MYSQL Platform: {e}") 
            with open("output.log", "a") as outfile:
                outfile.write(f"- Error connecting to MYSQL Platform: {e}\n")
            sys.exit(1)
        mycursor = mydb.cursor()
        mainquerry = ("SHOW DATABASES")
        listdbs = []
        mycursor.execute(mainquerry)
        print("Список баз данных:")
        with open("output.log", "a") as outfile:
            outfile.write("+ Отображаю список БД."+"\n")
        for mainquerry in mycursor:
            #print(mainquerry[0])
            listdbs.append(mainquerry[0])
        print(listdbs)
    elif choicecmd == '2':
        # В какой базе находится определенная таблица.
        with open("output.log", "a") as outfile:
                outfile.write("... Подключаюсь к БД."+"\n")
        try: 
            mydb = mysql.connector.connect(
                host="Ip_Nokia",
                user="tuser",
                password="tpassword",
            )
            with open("output.log", "a") as outfile:
                    outfile.write("+ Успешное подключение к БД."+"\n")
        except mysqldb.Error as e: 
            print(f"Error connecting to MYSQL Platform: {e}") 
            with open("output.log", "a") as outfile:
                outfile.write(f"- Error connecting to MYSQL Platform: {e}\n")
            sys.exit(1)
        mycursor = mydb.cursor()
        listdbs = []
        listtbs = []
        querrydb = ("SHOW DATABASES")
        mycursor.execute(querrydb)
        for querrydb in mycursor:
            #print(querrydb[0])
            listdbs.append(querrydb[0])
        with open("output.log", "a") as outfile:
            outfile.write("+ Отображаю список БД."+"\n")
        print("Какую таблицу хотите найти: ")
        choicetab = input()
        with open("output.log", "a") as outfile:
            outfile.write("+ Поиск таблицы: "+choicetab+"\n")
        for db in listdbs:
            querrytbs = "SHOW TABLES FROM " + db
            #print(querrytbs)
            mycursor.execute(querrytbs)
            for querrytbs in mycursor:
                listtbs.append(querrytbs[0])
                if querrytbs[0] == choicetab:
                    print(f"Table Name: {querrytbs[0]} Database Name: {db}")
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Нашел таблицу в базе "+db+"\n") 
                else:
                    #print("FALSE")
                    continue        
        print("Список таблиц:")
        print(listtbs)
        with open("output.log", "a") as outfile:
            outfile.write("+ выгрузил список таблиц из базы\n") 
    elif choicecmd == '3':
        # Найти таблицу, который находит определенный столбец во всей базе данных. 
    else:
        print("Введите y/n")        
    repeat = input("Do you want to continue? (y/n): ")
    if repeat == "n":
        break
    else:
        print("Введите y/n")