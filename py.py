import pandas as pd
import os
import re
import numpy as np
import mysql.connector

def checkCes2gEr(table):
    #12 Изменить программу таким образом, чтобы она выгружала данные из CES через базу данных и оптимизировать код.
    listdbs = []
    listrow = []

    try: 
        mydb = mysql.connector.connect(
            host="tipEr",
            user="tuser",
            password="tpassword",
        )
    except mysql.connector.errors.ProgrammingError:
        print("Error connecting to MYSQL Platform")
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")

    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")

    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        #print(querrydbs[0])
        listdbs.append(querrydbs[0])
    #listdbsdubl = list(set(listdbs))
    print("Список схем баз данных у Ericsson:")
    print(listdbs)
    with open("output.log", "a") as outfile:
        outfile.write("+ Got a list of databases\n")

    for db in listdbs:
        #print(db)
        if "tdb" == db:
            with open("output.log", "a") as outfile:
                outfile.write("... Database filter\n")
            try:
                querry2gEr = "SELECT BSS, Reg, BS_name, CELL FROM tdb.table_ericsson_2g_v WHERE BSS IS NULL ORDER BY Date DESC"
                mycursor.execute(querry2gEr)
                result = mycursor.fetchall()
                for row in result:
                    #print(row)
                    #print(type(row))
                    listrow.append(row)
                    with open("output.log", "a") as outfile:
                        outfile.write("+ got a table from the database\n")
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    #print("Список (listrow) с незаполненными данными 2G из CES:")
    #print(listrow)

    table = pd.DataFrame(listrow, columns =['BSS', 'Reg', 'BS_name', 'Sector_name'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added tables from the CES\n")

    table = table[table["Reg"].isin(listRegCes)]
    with open("output.log", "a") as outfile:
        outfile.write("+ corrected tables from the CES\n")
    mycursor.close()
    mydb.close()
    return table
def checkCes4gEr(table):
    listdbs = []
    listrow = []

    try: 
        mydb = mysql.connector.connect(
            host="tipEr",
            user="tuser",
            password="tpassword",
        )
    except mysql.connector.errors.ProgrammingError:
        print("Error connecting to MYSQL Platform")
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")

    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")

    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        #print(querrydbs[0])
        listdbs.append(querrydbs[0])
    #listdbsdubl = list(set(listdbs))
    #print("Список схем баз данных:")
    #print(listdbs)
    with open("output.log", "a") as outfile:
        outfile.write("+ Got a list of databases\n")

    for db in listdbs:
        #print(db)
        if "tdb" == db:
            with open("output.log", "a") as outfile:
                outfile.write("... Database filter\n")
            try:
                querry4gEr = "SELECT BSS, Reg, System_module_name_4G, Sector_name FROM tdb.table_ericsson_4g_v WHERE BSS IS NULL ORDER BY Date DESC"
                mycursor.execute(querry4gEr)
                result = mycursor.fetchall()
                for row in result:
                    #print(row)
                    listrow.append(row)
                    with open("output.log", "a") as outfile:
                        outfile.write("+ got a table from the database\n")
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    #print("Список (listrow) с незаполненными данными 4G из CES:")
    #print(listrow)

    table = pd.DataFrame(listrow, columns =['BSS', 'Reg', 'BS_name', 'Sector_name'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added tables from the CES\n")

    table = table[table["Reg"].isin(listRegCes)]
    with open("output.log", "a") as outfile:
        outfile.write("+ corrected tables from the CES\n")
    mycursor.close()    
    mydb.close()
    return table
def checkCes2gNok(table):
    listdbs = []
    listrow = []

    try: 
        mydb = mysql.connector.connect(
            host="tipNok",
            user="tuser",
            password="tpassword",
        )
    except mysql.connector.errors.ProgrammingError:
        print("Error connecting to MYSQL Platform")
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")

    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")

    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        #print(querrydbs[0])
        listdbs.append(querrydbs[0])
    #listdbsdubl = list(set(listdbs))
    print("Список схем баз данных у Nokia:")
    print(listdbs)
    with open("output.log", "a") as outfile:
        outfile.write("+ Got a list of databases\n")

    for db in listdbs:
        #print(db)
        if "tdb" == db:
            with open("output.log", "a") as outfile:
                outfile.write("... Database filter\n")
            try:
                querry2gNok = "SELECT BSS, Reg, BS_number, BS_name, CELL FROM tdb.table_nokia_2g_v WHERE BSS IS NULL ORDER BY Date DESC"
                mycursor.execute(querry2gNok)
                result = mycursor.fetchall()
                for row in result:
                    #print(row)
                    #print(type(row))
                    listrow.append(row)
                    with open("output.log", "a") as outfile:
                        outfile.write("+ got a table from the database\n")
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    #print("Список (listrow) с незаполненными данными 2G из CES:")
    #print(listrow)

    table = pd.DataFrame(listrow, columns =['BSS', 'Reg', 'BS_number', 'BS_name', 'Sector_name'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added tables from the CES\n")

    table = table[table["Reg"].isin(listRegCes)]
    with open("output.log", "a") as outfile:
        outfile.write("+ corrected tables from the CES\n")

    #9 Добработать программу так, чтобы она корректно считывала данные для базовых станций IO.
    addcol=table["BS_name"]
    table.insert(1, "ifRegIO", addcol)
    table["ifRegIO"] = table["ifRegIO"].str[:2]
    table["BS_name"] = table["BS_name"].str.replace("^IO", "IR", regex=True)
    table.insert(1, "ifBSnameIO", addcol)
    with open("output.log", "a") as outfile:
        outfile.write("+ corrected tables from the CES\n")
    mycursor.close()
    mydb.close()
    return table
def checkCes4gNok(table):
    listdbs = []
    listrow = []

    try: 
        mydb = mysql.connector.connect(
            host="tipNok",
            user="tuser",
            password="tpassword",
        )
    except mysql.connector.errors.ProgrammingError:
        print("Error connecting to MYSQL Platform")
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")

    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")

    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        #print(querrydbs[0])
        listdbs.append(querrydbs[0])
    #listdbsdubl = list(set(listdbs))
    #print("Список схем баз данных:")
    #print(listdbs)
    with open("output.log", "a") as outfile:
        outfile.write("+ Got a list of databases\n")

    for db in listdbs:
        #print(db)
        if "tdb" == db:
            with open("output.log", "a") as outfile:
                outfile.write("... Database filter\n")
            try:
                querry2gNok = "SELECT BSS, Reg, BS_name, Sector_name FROM tdb.table_nokia_4g_v WHERE BSS IS NULL ORDER BY Date DESC"
                mycursor.execute(querry2gNok)
                result = mycursor.fetchall()
                for row in result:
                    #print(row)
                    #print(type(row))
                    listrow.append(row)
                    with open("output.log", "a") as outfile:
                        outfile.write("+ got a table from the database\n")
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    #print("Список (listrow) с незаполненными данными из CES:")
    #print(listrow)

    table = pd.DataFrame(listrow, columns =['BSS', 'Reg', 'BS_name', 'Sector_name'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added tables from the CES\n")

    table = table[table["Reg"].isin(listRegCes)]
    with open("output.log", "a") as outfile:
        outfile.write("+ corrected tables from the CES\n")

    #9 Добработать программу так, чтобы она корректно считывала данные для базовых станций IO.
    addcol=table["BS_name"]
    table.insert(1, "ifRegIO", addcol)
    table["ifRegIO"] = table["ifRegIO"].str[:2]
    table["BS_name"] = table["BS_name"].str.replace("^IO", "IR", regex=True)
    table.insert(1, "ifBSnameIO", addcol)
    with open("output.log", "a") as outfile:
        outfile.write("+ corrected tables from the CES\n")
    mycursor.close()
    mydb.close()
    return table
def checkTable(table):
    return table.empty
def showWeekly2gNok(table):
    for file in listFiles:
        print("...Считываю данные из файла: ", file)
        with open("output.log", "a") as outfile:
            outfile.write("... Reading data from a file: "+file+"\n")

        if "N_" in file:
            cols = ['bsName','$dn','nwName', 'locationAreaIdLAC', 'rac']

            print("В файле "+file+" данные из еженедельной выгрузки Nokia")
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a Nokia: "+file+"\n")

            table = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="bts")
            with open("output.log", "a") as outfile:
                outfile.write("+ File contents received "+file+"\n")
        else:
            continue
    return table
def showWeekly4gNok(table):
    for file in listFiles:
        print("...Считываю данные из файла: ", file)
        with open("output.log", "a") as outfile:
            outfile.write("... Reading data from a file: "+file+"\n")

        if "N_" in file:
            cols = ['bsName','cellName', 'tac']

            print("В файле "+file+" данные из еженедельной выгрузки Nokia")
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a Nokia: "+file+"\n")

            table = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="lncel")
            with open("output.log", "a") as outfile:
                outfile.write("+ File contents received "+file+"\n")
        else:
            continue
    return table
def showWeekly2gEr(table):
    for file in listFiles:
        print("...Считываю данные из файла: ", file)
        with open("output.log", "a") as outfile:
            outfile.write("... Reading data from a file: "+file+"\n")

        if "Er_" in file:
            cols = ['NodeId','GeranCellId','LAC']

            print("В файле "+file+" данные из еженедельной выгрузки Ericsson")
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a Ericsson: "+file+"\n")

            table = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="GeranCell")
            with open("output.log", "a") as outfile:
                outfile.write("+ File contents received "+file+"\n")

            copycol=table["GeranCellId"]
            table.insert(1, "bsName", copycol)
            table["bsName"] = table["bsName"].str[:6]
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrceted a table with data from weekly download\n")
        else:
            continue
    return table
def showWeekly4gEr(table):
    for file in listFiles:
        print("...Считываю данные из файла: ", file)
        with open("output.log", "a") as outfile:
            outfile.write("... Reading data from a file: "+file+"\n")

        if "Er_" in file:
            cols = ['NodeId','EUtranCellTDDId','tac']
            print("В файле "+file+" данные из еженедельной выгрузки Ericsson")
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a Ericsson: "+file+"\n")
            table = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="EUtrancellxDD")
            with open("output.log", "a") as outfile:
                outfile.write("+ added tables from weekly download\n")
            copycol=table["EUtranCellTDDId"]
            table.insert(1, "bsName", copycol)
            table["bsName"] = table["bsName"].str[:6]
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrceted a table with data from weekly download\n")
        else:
            continue
    return table
def showOldBs(table):
    for file in listFiles:
        cols = ['index','longitude','latitude','BSC','LAC']

        print("...Считываю данные из файла: ", file)
        with open("output.log", "a") as outfile:
            outfile.write("... Reading data from a file: "+file+"\n")
        #5 Добавить данные LAC и BSC в таблицу и в пустой словарь название БС, координаты, LAC И BSC.
        #11 Написать отдельную программу, для выгрузки координат, контроллеров и Lac старых сайтов.
        if "google" in file:
            print("В файле "+file+" данные старых сайтов")
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a Google Earth: "+file+"\n")
            
            table = pd.read_excel(locDir+"/"+file, usecols=cols)
            with open("output.log", "a") as outfile:
                outfile.write("+ added tables from weekly download\n")

            #10 Найти ближайшего соседа базовой станции по формуле sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)):
            delcol=table["index"]
            table=table.drop("index", axis=1)
            table.insert(1, "oldbs", delcol)
            delcol=table["longitude"]
            table=table.drop("longitude", axis=1)
            table.insert(1, "longitudeY2", delcol)
            delcol=table["latitude"]
            table=table.drop("latitude", axis=1)
            table.insert(1, "latitudeX2", delcol)
            copycol=table["oldbs"]
            table.insert(1, "reg", copycol)
            table["reg"] = table["reg"].str[:2]
            with open("output.log", "a") as outfile:
                outfile.write(".+ Corrected tables from weekly download\n")
        else:
            continue
    return table
def showNewBs(table):
    prefixs = []
    newBsList = []
    coordList = [] 
    dataNewSites = dict()
    
    for file in listFiles:
        print("...Считываю данные из файла: ", file)
        with open("output.log", "a") as outfile:
            outfile.write("... Reading data from a file: "+file+"\n")

        if "Site_" in file:
            print("В файле "+file+" данные из сайта RDB")
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a: "+file+"\n")
            with open(locDir+"/"+file,"r", encoding="utf8") as rdbFile:
                contentFile = rdbFile.read()
            #print(contentFile)
            with open("output.log", "a") as outfile:
                outfile.write("+ File contents received "+file+"\n")
            Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", contentFile, re.DOTALL)

            for linePlacemark in Placemark:
                #print(linePlacemark)
                listBs = re.findall(r"<name>(.*?)</name>", linePlacemark, re.DOTALL)

                #print(listBs)
                for bs in listBs:                    
                    if "/" in bs:
                        bs = bs.split("/")[0]
                        bs = bs[:2] + bs[4:]
                        #print(bs)
                        prefix = bs[:2]
                        #print(prefix)
                        if prefix in listRegCes:
                            newBsList.append(bs)
                            prefixs.append(prefix)
                            prefixs = list(dict.fromkeys(prefixs))
                        #9 Добработать программу так, чтобы она считывала данные IO.
                        elif prefix == "IO":
                            print("... Корректировка префикса:")
                            print(bs)
                            print(prefix)                               
                            bs=bs.replace("IO","IR")
                            prefix = prefix.replace("IO","IR")
                            print(bs)
                            print(prefix)
                            newBsList.append(bs)
                            prefixs.append(prefix)
                            prefixs = list(dict.fromkeys(prefixs))
                        else:
                            print("Префикс не соответсвует формату")
                            with open("output.log", "a") as outfile:
                                outfile.write("- The prefix does not match the format "+prefix+"\n")
                    else:
                        print("Название базовой станции другого формата!")
                        with open("output.log", "a") as outfile:
                            outfile.write("- Название базовой станции другого формата!\n")

            coordinates = re.findall(r"<coordinates>(.*?)</coordinates>", linePlacemark, re.DOTALL)

            for coords in coordinates:
                #print(coords)
                longitude = coords.split(',')[0]
                latitude = coords.split(',')[1]
                #print(longitude + " " + latitude + "\n")
                coordList.append(longitude)
                coordList.append(latitude)

            remainder = (len(coordList)//len(newBsList))

            for numeration in range(len(newBsList)):
                dataNewSites[newBsList[numeration]] = [coordList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]

            cols = ["longitudeY1", "latitudeX1"]        
            table = pd.DataFrame.from_dict(dataNewSites, orient='index', columns=cols)
            table = table.reset_index()
            with open("output.log", "a") as outfile:
                outfile.write("+ Added Table (newDataTable) with data of new base stations from RDB\n")
            delcol=table["index"]
            table=table.drop("index", axis=1)
            table.insert(1, "newbs", delcol)
            copycol=table["newbs"]
            table.insert(1, "reg", copycol)
            table["reg"] = table["reg"].str[:2]
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrected Table (table) with data of new base stations from RDB\n")
        else:
            continue
    
    #print("Список новых базовых станций:")
    #print(newBsList)
    #print("Список координат станций:")
    #print(coordList)
    #print("Список новых базовых станций их координат:")
    #print(dataNewSites)
    return table
def findNeighbour(table):
    x1=table["latitudeX1"].astype(float)
    x2=table["latitudeX2"].astype(float)
    y1=table["longitudeY1"].astype(float)
    y2=table["longitudeY2"].astype(float)        
    with open("output.log", "a") as outfile:
        outfile.write("... Changing the data type of coordinates\n")
    table["distance"] = ""
    table["distance"] = np.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))
    with open("output.log", "a") as outfile:
        outfile.write("... Calculation of the distance between two base stations using the formula\n")
    #print(table.dtypes)
    groupedData = table.groupby("newbs")
    minDistance = groupedData["distance"].min()
    #print(minDistance)
    with open("output.log", "a") as outfile:
        outfile.write("... Finding the shortest distance\n")
    minDistanceTable = minDistance.reset_index()
    #print(minDistanceTable)
    table = pd.merge(minDistanceTable, table, left_on='distance', right_on='distance', how='inner')
    with open("output.log", "a") as outfile:
        outfile.write("+ The table (neighbourTable) that finds the neighbourhoods of new base stations using the formula has been adjusted\n")
    return table

listRegCes = ["VV","BU","IO","IR","SA","MD","KM","HB"]
listCmd = ["Заполненние данных для новых сайтов Nokia (1)", "Заполненние данных для новых сайтов Ericsson (2)", "Заполненние данных для довесов Nokia (3)", "Заполненние данных для довесов Ericsson (4)",  "Объединить таблицы довесов БС с новыми сайтами (5)"]
bscTemplateDict = {"891018":"BIR067", "28":"IRK028", "120":"IRK120", "396402":"IRK135", "400877":"IRK148", "401257":"IRK169", "401256":"IRK395", "401255":"IRK484", "398493":"KAM070", "912222":"KHB173", "394228":"KHB174", "398471":"MGD069", "324697":"NSK042", "138":"IRK138", "398453":"SAH068", "102":"SAH102", "318":"BRT318", "497":"BRT497", "140":"PRM140", "321":"VLD321", "322":"VLD322"}
ces2gErTable = pd.DataFrame()
ces4gErTable = pd.DataFrame()
ces2gNokTable = pd.DataFrame()
ces4gNokTable = pd.DataFrame()
weekly2gNokTable = pd.DataFrame()
weekly4gNokTable = pd.DataFrame()
weekly2gErTable = pd.DataFrame()
weekly4gErTable = pd.DataFrame()
oldDataTable = pd.DataFrame()
newDataTable = pd.DataFrame()
oldBs4gTableEr = pd.DataFrame()
oldBs4gTableNok = pd.DataFrame()
oldBs2gTableEr = pd.DataFrame()
oldBs2gTableNok = pd.DataFrame()
locDir = "unloading/"

#print("+ Создан лог файл output.log")
with open("output.log", "w") as outfile:
    outfile.write("+ created Log file output.log\n")

#2 Найти незаполненные строки БС в таблице из CES для каждых технологий - 2g, 4g.
ces2gErTable = checkCes2gEr(ces2gErTable)
ces4gErTable = checkCes4gEr(ces4gErTable)
ces2gNokTable = checkCes2gNok(ces2gNokTable)
ces4gNokTable = checkCes4gNok(ces4gNokTable)
print("Твблица (ces2gErTable, ces4gErTable, ces2gNokTable, ces4gNokTable) с незаполненными данными из CES:")
print(ces2gErTable)
print(ces4gErTable)
print("НУЖНО ПРОВЕРИТЬ ДАННЫЕ С NOKIA 2G 4G")
print(ces2gNokTable)
print(ces4gNokTable)
print("ces2gErTable -", checkTable(ces2gErTable))
print("ces4gErTable -", checkTable(ces4gErTable))
print("ces2gNokTable -", checkTable(ces2gNokTable))
print("ces4gNokTable -", checkTable(ces4gNokTable))
listFiles = os.listdir(locDir)
print("Список загруженных файлов в unloading: ", listFiles)
with open("output.log", "a") as outfile:
    outfile.write("... Checking for files in the folder "+locDir+"\n")
#3 Добавить имееющиеся данные в таблице из еженедельной выгрузки.
weekly2gNokTable = showWeekly2gNok(weekly2gNokTable)
weekly4gNokTable = showWeekly4gNok(weekly4gNokTable)
weekly2gErTable = showWeekly2gEr(weekly2gErTable)
weekly4gErTable = showWeekly4gEr(weekly4gErTable)
print("Таблица (weekly2gNokTable, weekly4gNokTable, weekly2gErTable, weekly4gErTable) из еженедельной выгрузки:")
#print(weekly2gNokTable)
#print(weekly4gNokTable)
#print(weekly2gErTable)
#print(weekly4gErTable)
oldDataTable = showOldBs(oldDataTable)
#print("Таблица (oldDataTable) из выгрузки Google Earth:")
#print(oldDataTable)
#4 Добавить данные координат в таблицу из rdb.
newDataTable = showNewBs(newDataTable)
print("Таблица (newDataTable) новых сайтов из RDB (Довесов тут быть не должно):")
print(newDataTable)
#print(bscTemplate)
bscTemplateTable = pd.DataFrame(list(bscTemplateDict.items()), columns=['Key', 'Values'])
print("Таблицa bscTemplateTable с шаблонными данными BSC:")
print(bscTemplateTable)
with open("output.log", "a") as outfile:
    outfile.write("+ Added Tables (allBs2gTable, allBs4gTable) for joining tables newBs2gTable and oldBs2gTable\n")

while True:
    #1 перечислить список команд, которые может выполнить программа:
    print("Список доступных команд: ", listCmd)
    print("ВНИМАНИЕ! Перед выполнением программы обновите файлы в папке unloading.")
    choiceCmd = input("Выполните действия: ")
    #print(choiceCmd)

    match choiceCmd:
        case "1":
            print("+ Выбрано действие - Заполненние данных для БС Nokia")
            with open("output.log", "a") as outfile:
                outfile.write("+ Action selected - Filling in data for Nokia BS\n")

            if checkTable(ces2gNokTable)==False and checkTable(ces4gNokTable)==False:
            #if checkTable(ces2gNokTable)==True and checkTable(ces4gNokTable)==True: #Temp
                print("Можно заполнять новые сайты")
                oldDataTable = oldDataTable[oldDataTable["reg"].isin(listRegCes[2:])]
                newDataTable = newDataTable[newDataTable["reg"].isin(listRegCes[2:])]
                print("Таблица (oldDataTable) из выгрузки Google Earth:")
                print(oldDataTable)
                print("Таблица (newDataTable) из RDB")
                print(newDataTable)
                neighbourTable = newDataTable.merge(oldDataTable, how='cross')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table (neighbourTable) connecting new base stations with old base stations\n")
                #6 Найти ближайшего соседа базовой станции по формуле sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)).
                neighbourTable = findNeighbour(neighbourTable)
                print("Таблица (neighbourTable), соединяющая новые базовые станции с соседними станциями по формуле:")
                print(neighbourTable)
                newBs2gTable = pd.merge(neighbourTable, ces2gNokTable, left_on='newbs_x', right_on='ifBSnameIO', how='inner')
                newBs4gTable = pd.merge(neighbourTable, ces4gNokTable, left_on='newbs_x', right_on='ifBSnameIO', how='inner')
                with open("output.log", "a") as outfile:
                    outfile.write(".+ Added tables (newBs2gTable, newBs4gTable) adding sector names from CES tables\n")
                print("Таблицы (newBs2gTable, newBs4gTable) добавляющие название секторов из таблиц CES:")
                print(newBs2gTable)
                print(newBs4gTable)
                print(checkTable(newBs2gTable))
                print(checkTable(newBs4gTable))

                if checkTable(newBs2gTable)==True or checkTable(newBs4gTable)==True or (checkTable(newBs2gTable)==True and checkTable(newBs4gTable)==True):
                    print("Нетю данных по новых сайтов в CES или нужно подкорректировать программу для новых сайтов!")
                    continue
                elif checkTable(newBs2gTable)==False and checkTable(newBs4gTable)==False:
                    print("Можно дальше искать rac для БС")
                    weekly2gNokTable = weekly2gNokTable.drop(["nwName", "$dn"], axis=1)
                    weekly2gNokTable = weekly2gNokTable.drop_duplicates()
                    weekly4gNokTable = weekly4gNokTable.drop("cellName", axis=1)
                    weekly4gNokTable = weekly4gNokTable.drop_duplicates()
                    with open("output.log", "a") as outfile:
                        outfile.write(".+ Corrected tables (weekly2gTable, weekly4gNokTable)\n")
                    #print("Таблицы (weekly2gNokTable, weekly4gNokTable) из еженедельной выгрузки Nokia:")
                    #print(weekly2gNokTable)
                    #print(weekly4gNokTable)
                    newBs2gTable = pd.merge(newBs2gTable, weekly2gNokTable, left_on='oldbs', right_on='bsName', how='inner')
                    newBs4gTable = pd.merge(newBs4gTable, weekly4gNokTable, left_on='oldbs', right_on='bsName', how='inner')
                    with open("output.log", "a") as outfile:
                        outfile.write(".+ Corrected tables (newBs2gTable, newBs4gTable) adding RAC from weekly uploading tables\n")
                    #print("Таблицы (newBs2gTable, newBs4gTable) добавляющие Rac из таблиц еженедельной выгрузки:")
                    #print(newBs2gTable)
                    #print(newBs4gTable)
                    #8 Замена строк в таблицах.
                    newBs2gTable = pd.merge(newBs2gTable, bscTemplateTable, left_on='BSC', right_on='Key', how='inner')
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Added to the table (newBs2gTable) column Values, To replace data in the BSC column\n")
                    #print("Таблицы (newBs2gTable, newBs4gTable) меняющий названия контроллеров:")
                    #print(newBs2gTable)
                    #print(newBs4gTable)
                    newBs2gTable=newBs2gTable.drop("newbs_x", axis=1)
                    newBs2gTable=newBs2gTable.drop("distance", axis=1)
                    newBs2gTable=newBs2gTable.drop("newbs_y", axis=1)
                    newBs2gTable=newBs2gTable.drop("longitudeY1", axis=1)
                    newBs2gTable=newBs2gTable.drop("latitudeX1", axis=1)
                    newBs2gTable=newBs2gTable.drop("oldbs", axis=1)
                    newBs2gTable=newBs2gTable.drop("longitudeY2", axis=1)
                    newBs2gTable=newBs2gTable.drop("latitudeX2", axis=1)
                    newBs2gTable=newBs2gTable.drop("BSC", axis=1)
                    newBs2gTable=newBs2gTable.drop("LAC", axis=1)
                    newBs2gTable=newBs2gTable.drop("BSS", axis=1)
                    newBs2gTable=newBs2gTable.drop("Reg", axis=1)
                    newBs2gTable=newBs2gTable.drop("BS_name", axis=1)
                    newBs2gTable=newBs2gTable.drop("BS_address", axis=1)
                    newBs2gTable=newBs2gTable.drop("ANT", axis=1)
                    newBs2gTable=newBs2gTable.drop("Имя сайта", axis=1)
                    newBs2gTable=newBs2gTable.drop("Key", axis=1)
                    newBs2gTable=newBs2gTable.drop("ifBSnameIO", axis=1)        
                    newBs2gTable["SW"]="MR10"
                    newBs4gTable=newBs4gTable.drop("newbs_x", axis=1)
                    newBs4gTable=newBs4gTable.drop("distance", axis=1)
                    newBs4gTable=newBs4gTable.drop("newbs_y", axis=1)
                    newBs4gTable=newBs4gTable.drop("longitudeY1", axis=1)
                    newBs4gTable=newBs4gTable.drop("latitudeX1", axis=1)
                    newBs4gTable=newBs4gTable.drop("oldbs", axis=1)
                    newBs4gTable=newBs4gTable.drop("longitudeY2", axis=1)
                    newBs4gTable=newBs4gTable.drop("latitudeX2", axis=1)
                    newBs4gTable=newBs4gTable.drop("BSC", axis=1)
                    newBs4gTable=newBs4gTable.drop("LAC", axis=1)
                    newBs4gTable=newBs4gTable.drop("BSS", axis=1)
                    newBs4gTable=newBs4gTable.drop("Reg", axis=1)
                    newBs4gTable=newBs4gTable.drop("Имя сайта_x", axis=1)
                    newBs4gTable=newBs4gTable.drop("RMOD", axis=1)
                    newBs4gTable=newBs4gTable.drop("EXT_port_on_System_module", axis=1)
                    newBs4gTable=newBs4gTable.drop("pMax", axis=1)        
                    newBs4gTable=newBs4gTable.drop("Имя сайта_y", axis=1)
                    newBs4gTable = newBs4gTable.drop_duplicates()
                    newBs2gTable = newBs2gTable.reindex(columns=["ifRegIO", "CELL", "SW", "Values", "BS_number", "locationAreaIdLAC", "rac"])
                    newBs4gTable = newBs4gTable.reindex(columns=["ifRegIO", "Имя системного модуля", "Sector_name", "tac"])
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Corrected the Table (newBs2gTable, newBs4gTable)\n")
                    print("Таблицы (newBs2gTable, newBs4gTable):")
                    print(newBs2gTable)
                    print(newBs4gTable)
                    #7 Добавить файл csv данные, полученн1ые из таблиц.   
                    newBs2gTable.to_csv('newBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                    newBs4gTable.to_csv('newBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Added files to import to the site newBs2gTable и newBs4gTable \n")
            else:
                print("Нету данных по новых сайтов в CES или нужно подкорректировать программу для новых сайтов!")
        case "2":
            #10 Добавить аналогичным образом данные для технологий Ericsson.
            print("+ Выбрано действие - Заполненние данных для БС Ericsson")
            with open("output.log", "a") as outfile:
                outfile.write("+ Action selected - Filling in data for Ericsson BS\n")

            if checkTable(ces2gErTable)==False and checkTable(ces4gErTable)==False:
                print("Можно заполнять новые сайты")
                oldDataTable = oldDataTable[oldDataTable["reg"].isin(listRegCes[:2])]
                newDataTable = newDataTable[newDataTable["reg"].isin(listRegCes[:2])]
                print("Таблица (newDataTable) из RDB")
                print(newDataTable)
                neighbourTable = newDataTable.merge(oldDataTable, how='cross')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table (neighbourTable) connecting new base stations with old base stations\n")
                neighbourTable = findNeighbour(neighbourTable)
                print("Таблица (neighbourTable), соединяющая новые базовые станции с соседними станциями по формуле:")
                print(neighbourTable)

                #newBs2gTable = pd.merge(neighbourTable, ces2gNokTable, left_on='newbs_x', right_on='ifBSnameIO', how='inner')
                #newBs4gTable = pd.merge(neighbourTable, ces4gNokTable, left_on='newbs_x', right_on='ifBSnameIO', how='inner')
                newBs2gTable = pd.merge(neighbourTable, ces2gTable, left_on='newbs_x', right_on='BS_name', how='inner')
                newBs4gTable = pd.merge(neighbourTable, ces4gTable, left_on='newbs_x', right_on='BS_name', how='inner')
                with open("output.log", "a") as outfile:
                    outfile.write(".+ Added tables (newBs2gTable, newBs4gTable) adding sector names from CES tables\n")
                print("Таблицы (newBs2gTable, newBs4gTable) добавляющие название секторов из таблиц CES:")
                print(newBs2gTable)
                print(newBs4gTable)
                print(checkTable(newBs2gTable))
                print(checkTable(newBs4gTable))

                if checkTable(newBs2gTable)==True or checkTable(newBs4gTable)==True or (checkTable(newBs2gTable)==True and checkTable(newBs4gTable)==True):
                    print("Нетю данных по новых сайтов в CES или нужно подкорректировать программу для новых сайтов!")
                    continue
                elif checkTable(newBs2gTable)==False and checkTable(newBs4gTable)==False:
                    print("Можно дальше искать rac для БС")
                    
                    newBs2gTable = pd.merge(newBs2gTable, bscTemplateTable, left_on='BSC', right_on='Key', how='inner')
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Added to the table (newBs2gTable) column Values, To replace data in the BSC column\n")
                    #print("Таблицы (newBs2gTable, newBs4gTable) меняющий названия контроллеров:")
                    #print(newBs2gTable)
                    #print(newBs4gTable)
                    newBs2gTable=newBs2gTable.drop("newbs_x", axis=1)
                    newBs2gTable=newBs2gTable.drop("distance", axis=1)
                    newBs2gTable=newBs2gTable.drop("newbs_y", axis=1)
                    newBs2gTable=newBs2gTable.drop("longitudeY1", axis=1)
                    newBs2gTable=newBs2gTable.drop("latitudeX1", axis=1)
                    newBs2gTable=newBs2gTable.drop("oldbs", axis=1)
                    newBs2gTable=newBs2gTable.drop("longitudeY2", axis=1)
                    newBs2gTable=newBs2gTable.drop("latitudeX2", axis=1)
                    newBs2gTable=newBs2gTable.drop("BSC", axis=1)
                    newBs2gTable=newBs2gTable.drop("BSS", axis=1)
                    newBs2gTable=newBs2gTable.drop("Subreg", axis=1)       
                    newBs2gTable=newBs2gTable.drop("External_Alarm", axis=1)
                    newBs2gTable=newBs2gTable.drop("BS_address", axis=1)
                    newBs2gTable=newBs2gTable.drop("Key", axis=1)
                    newBs2gTable["SW"]="-"
                    newBs2gTable["TG"]="0"
                    newBs2gTable["RBL2_1"]="-"
                    newBs2gTable["RBL2_2"]="-"
                    newBs2gTable["OETM_1"]="-"
                    newBs2gTable["OETM_2"]="-"
                    newBs4gTable=newBs4gTable.drop("Имя сайта", axis=1) 
                    newBs4gTable=newBs4gTable.drop("newbs_x", axis=1) 
                    newBs4gTable=newBs4gTable.drop("distance", axis=1)
                    newBs4gTable=newBs4gTable.drop("newbs_y", axis=1)
                    newBs4gTable=newBs4gTable.drop("longitudeY1", axis=1)
                    newBs4gTable=newBs4gTable.drop("latitudeX1", axis=1)
                    newBs4gTable=newBs4gTable.drop("oldbs", axis=1)
                    newBs4gTable=newBs4gTable.drop("longitudeY2", axis=1)
                    newBs4gTable=newBs4gTable.drop("latitudeX2", axis=1)
                    newBs4gTable=newBs4gTable.drop("BSC", axis=1)
                    newBs4gTable=newBs4gTable.drop("BSS", axis=1)
                    newBs4gTable=newBs4gTable.drop("Subreg", axis=1)
                    newBs4gTable=newBs4gTable.drop("LTE_Frequency", axis=1)
                    newBs4gTable=newBs4gTable.drop("RRUS", axis=1)
                    newBs2gTable = newBs2gTable.reindex(columns=["Reg", "BS_name", "Values", "TG", "Имя сайта", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "CELL"])
                    newBs4gTable = newBs4gTable.reindex(columns=["Reg", "System_module_name_4G", "LAC", "Sector_name"])
                    newBs4gTable = newBs4gTable.drop_duplicates()
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Corrected the Table (newBs2gTable, newBs4gTable)\n")
                    print("Таблицы (newBs2gTable, newBs4gTable):")
                    print(newBs2gTable)
                    print(newBs4gTable)
                    newBs2gTable.to_csv('newBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                    newBs4gTable.to_csv('newBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Added files to import to the site newBs2gTable и newBs4gTable \n")
            else:
                print("Так собирать данные нельзя или нужно подкорректировать программу для новых сайтов!")
        case "3":
            print("+ Выбрано действие - Заполненние данных для довесов Nokia")
            with open("output.log", "a") as outfile:
                outfile.write("+ Action selected - Filling in data for Nokia BS\n")
            
            if (checkTable(ces2gNokTable)==True and checkTable(ces4gNokTable)==False) or (checkTable(ces2gNokTable)==False and checkTable(ces4gNokTable)==False):
                #print("Можно заполнять 4G")
                oldBs4gTableNok = pd.merge(ces4gNokTable, weekly4gNokTable, left_on='ifBSnameIO', right_on='bsName', how='inner')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added tables (oldBs4gTableNok) with completed site\n")                
                oldBs4gTableNok = oldBs4gTableNok.drop("cellName", axis=1)
                oldBs4gTableNok = oldBs4gTableNok.drop_duplicates()
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected tables (oldBs4gTableNok) with completed site\n")
                oldBs4gTableNok = oldBs4gTableNok.drop(["BSS","Reg","BS_name","bsName"], axis=1)
                oldBs4gTableNok = oldBs4gTableNok.reindex(columns=["ifRegIO", "ifBSnameIO", "Sector_name", "tac"])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected tables (oldBs4gTableNok) with completed site\n")
                print("Таблица (oldBs4gTableNok) для довесов:")
                print(oldBs4gTableNok)
                oldBs4gTableNok.to_csv('oldBs4gTableNok.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added files to import to the site oldBs4gTableNok \n")
            else:
                print("Так собирать данные нельзя или нужно подкорректировать программу для довесов!")
        case "4":
            print("+ Выбрано действие - Заполненние данных для довесов Ericsson")
            with open("output.log", "a") as outfile:
                outfile.write("+ Action selected - Filling in data for Ericsson BS\n")
            
            if checkTable(ces2gErTable)==True and checkTable(ces4gErTable)==False:
                #print("Можно заполнять 4G")
                oldBs4gTableEr = pd.merge(ces4gErTable, weekly4gErTable, left_on='BS_name', right_on='NodeId', how='inner')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added tables (oldBs4gTableEr) with completed site\n")                
                oldBs4gTableEr = oldBs4gTableEr.drop("EUtranCellTDDId", axis=1)
                oldBs4gTableEr = oldBs4gTableEr.drop_duplicates()
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected tables (oldBs4gTableEr) with completed site\n")
                oldBs4gTableEr = oldBs4gTableEr.drop(["BSS","bsName"], axis=1)
                oldBs4gTableEr = oldBs4gTableEr.reindex(columns=["Reg", "BS_name", "tac", "Sector_name"])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected tables (oldBs4gTableEr) with completed site\n")
                print("Таблица (oldBs4gTableEr) для довесов:")
                print(oldBs4gTableEr)
                oldBs4gTableEr.to_csv('oldBs4gTableEr.csv', sep=',', index=False, header=False, encoding='UTF-8-SIG')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added files to import to the site oldBs4gTableEr \n")
            else:
                print("Так собирать данные нельзя или нужно подкорректировать программу для довесов!")
        case "5":
            #print("+ Выбрано действие - Объединить таблицы довесов БС с новыми сайтамиС")
            with open("output.log", "a") as outfile:
                outfile.write("+ Action selected - Filling in data for ALL sites BS\n")
            print("oldBs2gTableEr -", checkTable(oldBs2gTableEr))
            print("oldBs2gTableNok -", checkTable(oldBs2gTableNok))
            print("oldBs4gTableEr -", checkTable(oldBs4gTableEr))
            print("oldBs4gTableNok -", checkTable(oldBs4gTableNok))
            print("Таблицы (oldBs2gTableEr, oldBs4gTableEr, oldBs2gTableNok, oldBs4gTableNok):")
            print(oldBs2gTableEr)
            print(oldBs4gTableEr)
            print(oldBs2gTableNok)
            print(oldBs4gTableNok)

            if checkTable(oldBs2gTableEr)==False and checkTable(oldBs4gTableEr)==False:
                print("Будет доработка программы!")
                allBs2gTableEr = pd.concat([newBs2gTable,oldBs2gTableEr])
                allBs4gTableEr = pd.concat([newBs4gTable,oldBs4gTableEr])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added the Table (allBs2gTable, allBs4gTable) for all sites\n")
                #print("Таблицы (allBs2gTable, allBs4gTable) с довесами и новыми сайтамиg:")
                #print(allBs2gTable)
                #print(allBs4gTable)
                allBs2gTable.to_csv('allBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                allBs4gTable.to_csv('allBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added files to import to the site tempfile2g и tempfile4g \n")
        case _:
            print("- Некорректные действия!")
            with open("output.log", "a") as outfile:
                outfile.write("- Incorrect actions!\n")

    choiceContinue = input("Do you wish to continue? [y/n]: ").lower()

    while choiceContinue not in ['y', 'n']:
        choiceContinue = input("- Invalid input! Enter y/n: ").lower()    
    if choiceContinue in ['y']:
        state = 2 
    elif choiceContinue in ['n']:
        break
