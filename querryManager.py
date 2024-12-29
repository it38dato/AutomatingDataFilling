import mysql.connector
import sys
repeat="y"
with open("output.log", "w") as outfile:
    outfile.write("") 
while repeat == "y":
    print("Выполните действия от 1 до 2:")
    listcmd=['Показать список баз (1)', 'Найти таблицу в базе по определенным столбцам (2)', ]
    print(listcmd)
    choicecmd = input()
    #print(choicecmd)
    if choicecmd == '1':
        #1 Подключиться к базе.
        with open("output.log", "a") as outfile:
                outfile.write("... Подключаюсь к БД."+"\n")
        try: 
            mydb = mysql.connector.connect(
                host="ipNokia",
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
    else:
        print("Введите y/n")        
    repeat = input("Do you want to continue? (y/n): ")
    if repeat == "n":
        break
    else:
        print("Введите y/n")