import mysql.connector
#import sys
def qShowDbs():
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    with open("output.log", "a") as outfile:
        outfile.write("+ Отображаю список БД."+"\n")
    for querrydbs in mycursor:
        #print(querrydbs[0])
        listdbs.append(querrydbs[0])
    print("Список баз данных:")
    listdbsdubl = list(set(listdbs))
    print(listdbsdubl)
    return listdbs
repeat="y"
try: 
    with open("output.log", "a") as outfile:
        outfile.write("... Подключаюсь к БД."+"\n")
    mydb = mysql.connector.connect(
        host="tipNikoa",
        user="tuser",
        password="tpassword",
    )
    with open("output.log", "a") as outfile:
        outfile.write("+ Успешное подключение к БД."+"\n")
except mysql.connector.errors.ProgrammingError:
    print("Error connecting to MYSQL Platform")
    with open("output.log", "a") as outfile:
         outfile.write("- Error connecting to MYSQL Platform:\n")
mycursor = mydb.cursor()
with open("output.log", "w") as outfile:
    outfile.write("")
while repeat == "y":
    listcmd = [
        'Показать список баз (1)', 
        'В какой базе находится определенная таблица (2)', 
        'Найти строки во всей базе, в которой есть определенная имя базовая станции (3)', 
        'Найти строки в одной базе, в которой есть определенная имя базовая станции (4)', 
        'Выборка (5)'
    ]
    listdbs = []
    listtbs = []
    #localListDb = []    
    print(listcmd)
    choicecmd = input("Выполните действия от 1 до : ")
    #print(choicecmd)
    if choicecmd == '1':
        # Показать список баз
        qShowDbs()
    elif choicecmd == '2':
        # В какой базе находится определенная таблица.
        qShowDbs()       
        choicetab = input("Какую таблицу хотите найти: ")
        with open("output.log", "a") as outfile:
            outfile.write("+ Поиск таблицы: "+choicetab+"\n")
        for db in listdbs:
            querrytbs = "SHOW TABLES FROM " + db
            #print(querrytbs)
            mycursor.execute(querrytbs)
            for querrytbs in mycursor:
                listtbs.append(querrytbs[0])
                if querrytbs[0] == choicetab:
                    print(f"Table Name: {querrytbs[0]} ; Database Name: {db}")
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
        rowTable = input("Выберите столбец: ")
        lineData = input("Выберите объект, который хотите найти: ")        
        qShowDbs()
        for db in listdbs:
            #print(db)
            querrytbs = "SHOW TABLES FROM "+db
            #print(querrytbs)
            mycursor.execute(querrytbs)
            for tb in mycursor:
                #print(tb[0])
                listtbs.append(tb[0])
            #print(listtbs)
            for tb in listtbs:
                #print(tb)
                try:
                    querrysel = "SELECT * FROM "+db+"."+tb+" WHERE "+rowTable+"='"+lineData+"'"
                    #querrysel = "SELECT * FROM "+db+"."+tb+" WHERE BS_name='IO019'"
                    #print(querrysel)
                    mycursor.execute(querrysel)
                    result = mycursor.fetchall()
                    for row in result:
                        print(row)
                        print("Взято из Базы: "+db+" Таблицы: "+tb)
                except mysql.connector.errors.ProgrammingError:
                    #print("НЕТУ данной ячейки в такой таблице")
                    continue
                except mysql.connector.errors.DatabaseError:
                    #print("ЗАпрещено")
                    continue
    elif choicecmd == '4':
        # Найти строки в одной базе, в которой есть определенная имя базовая станции
        dbData = input("Выберите базу: ")
        rowTable = input("Выберите столбец: ")
        lineData = input("Выберите объект, который хотите найти: ")
        qShowDbs()
        for db in listdbs:
            #print(db)
            if dbData == db:
                querrytbs = "SHOW TABLES FROM "+db
                #print(querrytbs)
                mycursor.execute(querrytbs)
                for tb in mycursor:
                    #print(tb[0])
                    listtbs.append(tb[0])
                #print(listtbs)
                for tb in listtbs:
                    #print(tb)
                    try:
                        querrysel = "SELECT * FROM "+db+"."+tb+" WHERE "+rowTable+"='"+lineData+"'"
                        #querrysel = "SELECT * FROM "+db+"."+tb+" WHERE BS_name='IO019'"
                        #print(querrysel)
                        mycursor.execute(querrysel)
                        result = mycursor.fetchall()
                        for row in result:
                            print(row)
                            print("Взято из Базы: "+db+" Таблицы: "+tb)
                    except mysql.connector.errors.ProgrammingError:
                        #print("НЕТУ данной ячейки в такой таблице")
                        continue
                    except mysql.connector.errors.DatabaseError:
                        #print("ЗАпрещено")
                        continue
            else:
                continue
    elif choicecmd == '5':
        # Выборка. 
        querryDb = input("Выберите базу: ")
        querryCol = input("Выберите столбцы: ")
        querryTb = input("Выберите таблицу: ")
        querryConditions = input("Выберите условие: ")
        qShowDbs()
        for db in listdbs:
            #print(db)
            if querryDb == db:
                try:
                    querrySel = "SELECT "+querryCol+" FROM "+db+"."+querryTb+" "+querryConditions
                    #querrySel = "SELECT BSS, Reg, BS_name, CELL FROM tdb.table_ericsson_2g_v WHERE Reg='VV' AND BSS IS NULL ORDER BY Date DESC LIMIT 5"
                    #print(querrySel)
                    mycursor.execute(querrySel)
                    result = mycursor.fetchall()
                    for row in result:
                        print(row)
                        print("Взято из Базы: "+db+" Таблицы: "+querryTb)
                except mysql.connector.errors.ProgrammingError:
                    #print("НЕТУ данной ячейки в такой таблице")
                    continue
                except mysql.connector.errors.DatabaseError:
                    #print("ЗАпрещено")
                    continue
            else:
                continue
    else:
        print("Введите y/n")        



    repeat = input("Do you want to continue? (y/n): ")
    if repeat == "n":
        break
    else:
        print("Введите y/n")