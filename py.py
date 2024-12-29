import pandas as pd
import os
import re
import numpy as np
#1 перечислить список команд, которые может выполнить программа:
repeat="y"
with open("output.log", "w") as outfile:
    outfile.write("+ Создан лог файл output.log."+"\n") 
while repeat == "y":
    listCmd=["Заполненние данных для БС Nokia (1)", "Заполненние данных для БС Ericsson (2)"]
    print(listCmd)
    print("ВНИМАНИЕ! Перед выполнением программы добавьте файлы в папку unloading.") 
    choiceCmd = input("Выполните действия: ")    
    #print(choiceCmd)
    if choiceCmd == "1":
        #print("+ Выбрано действие - Заполненние данных для БС Nokia")
        with open("output.log", "a") as outfile:
            outfile.write("+ Выбрано действие - Заполненние данных для БС Nokia."+"\n")
        #2 Собрать в список данные, которые необходимо заполнить в шаблоне: 
        listData=["Reg","CELL","SW","BSC","BCF","LAC","RAC2g","Имя сайта","Sector_name","RAC3g","URA","RNC_ID"]
        print("Для заполнения нужны следующие данные: ", listData)
        #3 Найти незаполненные строки БС IR2468 в таблице из CES для каждых технологий - 2g, 4g:           
        pwd = "unloading/"
        netDir = "data/"
        listFiles = os.listdir(pwd)
        with open("output.log", "a") as outfile:
            outfile.write("... Проверяю наличие файлов в папке "+pwd+"\n")        
        print("Список загруженных файлов в unloading: ", listFiles)
        weekly2gTable = pd.DataFrame()
        weekly4gTable = pd.DataFrame() 
        newBsList = []
        prefixs = []
        coordList = [] 
        dataNewSites = dict()
        newDataTable = pd.DataFrame()
        ces2gTable = pd.DataFrame()
        ces4gTable = pd.DataFrame()
        oldBsList=[]
        oldDataList=[]
        dataOldSites = dict()
        oldDataTable = pd.DataFrame()
        minDistanceTable = pd.DataFrame()
        for file in listFiles:
            #print("Считываю данные из файла: ", file)
            with open("output.log", "a") as outfile:
                outfile.write("... Считываю данные из файла: "+file+"\n")
            #4 Добавить имееющиеся данные в таблице из еженедельной выгрузки:
            if "N_" in file:
                #print("Это еженедельная выгрузка из Nokia")
                cols = [1, 3, 8, 9]
                table2g = pd.read_excel(pwd+"/"+file, usecols=cols, sheet_name="bts")
                table4g = pd.read_excel(pwd+"/"+file, usecols=cols, sheet_name="lncel")
                #print(table2g)
                #print(table4g)
                with open("output.log", "a") as outfile:
                    outfile.write("+ Загружены в таблицы необходимые данные 2g, 4g из файла "+file+"\n")
                weekly2gTable = pd.concat([weekly2gTable,table2g])
                weekly4gTable = pd.concat([weekly4gTable,table4g])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Загружены в пустые таблицы необходимые данные 2g, 4g из файла "+file+"\n")
                #print("Успешно прочитал данные из файла: ", file)
            #5 Добавить данные координат в таблицу из rdb.:
            elif "Site_" in file:
                #print("Это выгрузка из сайта RDB")
                with open(pwd+"/"+file,"r", encoding="utf8") as rdbFile:
                    contentFile = rdbFile.read()
                #print(contentFile)
                with open("output.log", "a") as outfile:
                    outfile.write("+ Получено содержимое файла "+file+"\n")
                Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", contentFile, re.DOTALL)
                for linePlacemark in Placemark:
                    #print(linePlacemark)
                    with open("output.log", "a") as outfile:
                        outfile.write("... Чтение данных в Placemark\n")
                    listBs = re.findall(r"<name>(.*?)</name>", linePlacemark, re.DOTALL)
                    #print(listBs)
                    with open("output.log", "a") as outfile:
                        outfile.write("... Обработка и сортировка названий базовых станций\n")
                    for bs in listBs:
                        if "/" in bs:
                            bs = bs.split("/")[0]
                            #i1 = 2
                            #i2 = 3
                            #bs = bs[:i1] + bs[i2+1:]
                            bs = bs[:2] + bs[4:]
                            #print(bs)
                            newBsList.append(bs)
                            #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
                            prefix = bs[:2]
                            #print(prefix)
                            prefixs.append(prefix)
                            prefixs = list(dict.fromkeys(prefixs))                            
                            with open("output.log", "a") as outfile:
                                outfile.write("+ Получены названия базовых станций и префиксы из файла "+file+"\n")
                        else:
                            print("Название базовой станции другого формата!")
                            with open("output.log", "a") as outfile:
                                outfile.write("- Название базовой станции другого формата!\n")
                coordinates = re.findall(r"<coordinates>(.*?)</coordinates>", linePlacemark, re.DOTALL)
                with open("output.log", "a") as outfile:
                    outfile.write("... Обработка и сортировка координат базовых станций\n")
                for coords in coordinates:
                    #print(coords)
                    longitude = coords.split(',')[0]
                    latitude = coords.split(',')[1]
                    #print(longitude + " " + latitude + "\n")
                    coordList.append(longitude)
                    coordList.append(latitude)
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Получены координаты базовых станций из файла "+file+"\n")
                #print("Успешно прочитал данные из файла: ", file)
            else:
                #print("Это выгрузка из сайта CES")
                cols = [2, 6, 7, 8, 10, 14]
                table = pd.read_excel(pwd+"/"+file, usecols=cols)
                table = table[table["BSS"].isna()]
                #print(table)
                with open("output.log", "a") as outfile:
                    outfile.write("+ Получено содержимое файла "+file+"\n")
                if "BS_address" in table:
                    ces2gTable = pd.concat([ces2gTable,table])
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Загружены в таблицы необходимые данные 2g из файла "+file+"\n")
                elif "RMOD" in table:
                    ces4gTable = pd.concat([ces4gTable,table])
                    with open("output.log", "a") as outfile:
                        outfile.write("+ Загружены в таблицы необходимые данные 4g из файла "+file+"\n")
                else: 
                    with open("output.log", "a") as outfile:
                        outfile.write("- Некорректная таблица в файле "+file+"\n")
                #print(table)
                #print("Успешно прочитал данные из файла: ", file)
        #№print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки:")
        #print(weekly2gTable)
        #print(weekly4gTable)
        #print("Список новых базовых станций:")
        #print(newBsList)
        #print("Список координат станций:")
        #print(coordList)
        with open("output.log", "a") as outfile:
             outfile.write("... Добавление в пустой словарь названия базовых станций и координаты\n")
        remainder = (len(coordList)//len(newBsList))
        for numeration in range(len(newBsList)):
            dataNewSites[newBsList[numeration]] = [coordList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
        #print("Список новых базовых станций их координат:")
        #print(dataNewSites)
        with open("output.log", "a") as outfile:
            outfile.write("+ Добавлены названия и координаты базовых станций в словарь\n")
        cols = ["longitude", "latitude"]        
        newDataTable = pd.DataFrame.from_dict(dataNewSites, orient='index', columns=cols)
        newDataTable = newDataTable.reset_index()
        #print("Таблица (newDataTable) координат новых базовых станций:")
        #print(newDataTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Загружены в таблицы кординат для новых базовых станций из RDB файла\n")
        #print("Таблицы (ces2gTable, ces4gTable) 2g, 4g из сайта CES:")
        #print(ces2gTable)
        #print(ces4gTable)
        #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:        
        lengthDir = len(netDir)
        listReg = ["IRK","MGD","SAH","KHA","KAM"]
        for root, dirs, files in os.walk(netDir):
            with open("output.log", "a") as outfile:
                outfile.write("... Проверяю наличие файлов в папке "+netDir+"\n")
            allDir = root[lengthDir:]
            #print(allDir)
            with open("output.log", "a") as outfile:
                outfile.write("... Фильтрация лишних папок\n")
            if ("old" in allDir):
                continue
            elif allDir in listReg:
                #print(allDir)
                for kmlFile in files:
                    #print(kmlFile)
                    with open("output.log", "a") as outfile:
                        outfile.write("... Фильтрация лишних файлов\n")
                    if prefixs[0] in kmlFile:
                        #print("Это выгрузка из всех сайтов RDB")
                        #print(kmlFile)  
                        with open("output.log", "a") as outfile:
                            outfile.write("+ Получен необходимый файл "+kmlFile+" в папке "+netDir+"\n")
                        needDir = netDir+allDir+"/"+kmlFile
                        #print(needDir)
                        with open("output.log", "a") as outfile:
                            outfile.write("+ Получена необходимая папка "+needDir+", в которой находится файл "+kmlFile+"\n")                        
                        #with open(kmlFile,"r", encoding="utf8") as rdbFile:
                        with open(needDir,"r", encoding="utf8") as rdbFile:
                            file = rdbFile.read()
                        #print(file) 
                        with open("output.log", "a") as outfile:
                            outfile.write("... Считываю данные из файла: "+kmlFile+"\n")
                        #7 Добавить данные LAC и BSC в таблицу:
                        Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", file, re.DOTALL)
                        with open("output.log", "a") as outfile:
                            outfile.write("+ Получено содержимое файла: "+kmlFile+"\n")
                        for linePlacemark in Placemark:
                            #print(linePlacemark)
                            #with open("output.log", "a") as outfile:
                            #    outfile.write("... Чтение данных в Placemark\n")
                            if ("<longitude>" in linePlacemark) and ("LAC" in linePlacemark) and ("BSC: " in linePlacemark):
                                #print(linePlacemark)
                                if ("<longitude></longitude>" in linePlacemark) and ("<latitude></latitude>" in linePlacemark):
                                    with open("output.txt", "a") as outfile:
                                        outfile.write("- Недостающие данные (Координаты, LAC, BSC)!\n")
                                    continue
                                else:
                                    listBs = re.findall(r"<name>(.*?)</name>", linePlacemark, re.DOTALL)
                                    with open("output.txt", "a") as outfile:
                                        outfile.write("... Проверяю корректность заполнения названий БС, координат, LAC и BSC\n")
                                    for bs in listBs:
                                        if (len(bs)==6) == True:
                                            #print(bs)
                                            oldBsList.append(bs)
                                        else:
                                            with open("output.txt", "a") as outfile:
                                                outfile.write("Название базой станции "+ bs +" другого формата!\n")
                                            continue
                                    listСoords = re.findall(r"<longitude>(.*?)</latitude>", linePlacemark, re.DOTALL)
                                    for coords in listСoords:
                                        #print(coords)
                                        coordinates = coords.split("</longitude>\n     <latitude>")
                                        #print(coordinates)
                                        longitude = coordinates[0]
                                        latitude = coordinates[1]
                                        #print(longitude + " " + latitude + "\n")
                                        #with open("output.txt", "a") as outfile:
                                        #    outfile.write(longitude + " " + latitude + "\n")
                                        oldDataList.append(longitude)
                                        oldDataList.append(latitude)
                                    listBscTac = re.findall(r"<description>BSC: (.*?)</description>", linePlacemark, re.DOTALL)
                                    #print(listBscTac)
                                    for bsctac in listBscTac:
                                        #print(bsctac)
                                        data = bsctac.split(" LAC: ")
                                        #print(data)
                                        bsc = data[0]
                                        lac = data[1]
                                        #print(bsc + " " + lac + "\n")
                                        #with open("output.txt", "a") as outfile:
                                        #    outfile.write(bsc + " " + lac + "\n")
                                        oldDataList.append(bsc)
                                        oldDataList.append(lac)
                            elif ("<longitude>" in linePlacemark) and ("LAC" in linePlacemark) and ("URA: " in linePlacemark):
                                #print("ВОЗМОЖНО, эти данные понадобятся для заполнения 3g!")
                                #print(linePlacemark)
                                continue
                            else:
                                with open("output.txt", "a") as outfile:
                                    outfile.write("Недостающие данные (Координаты, Lac, BSC)!\n")
                                continue
            else:
                continue
        #8 Добавить в пустой словарь название БС, координаты, LAC И BSC:
        #print("Список старых базовых станций:")
        #print(oldBsList)
        #print("Список координат, LAC И BSC для старых базовых станций:")
        #print(oldDataList)
        #print("Список старых базовых станций, их координат, LAC И BSC:")
        remainder = (len(oldDataList)//len(oldBsList))
        for numeration in range(len(oldBsList)):
            dataOldSites[oldBsList[numeration]] = [oldDataList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
        #print(dataOldSites)
        with open("output.log", "a") as outfile:
            outfile.write("+ Добавлены названия базовых станций, координаты, LAC И BSC в словарь\n")
        #9 Добавить в пустую таблицу данные из словаря:
        cols = ["longitude", "latitude", "BSC", "LAC"]
        oldDataTable = pd.DataFrame.from_dict(dataOldSites, orient='index', columns=cols)
        oldDataTable = oldDataTable.reset_index()
        #print("Таблица (oldDataTable) координат, LAC И BSC старых базовых станций:")
        #print(oldDataTable)
        #10 Найти ближайшего соседа базовой станции по формуле sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)):
        delcol=oldDataTable["index"]
        oldDataTable=oldDataTable.drop("index", axis=1)
        oldDataTable.insert(0, "oldbs", delcol)
        delcol=oldDataTable["longitude"]
        oldDataTable=oldDataTable.drop("longitude", axis=1)
        oldDataTable.insert(1, "longitudeY2", delcol)
        delcol=oldDataTable["latitude"]
        oldDataTable=oldDataTable.drop("latitude", axis=1)
        oldDataTable.insert(2, "latitudeX2", delcol)
        #print("Таблица (oldDataTable) координат, LAC И BSC старых базовых станций:")
        #print(oldDataTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Подкорректирована таблица c координатами, LAC И BSC старых базовых станций\n")
        delcol=newDataTable["index"]
        newDataTable=newDataTable.drop("index", axis=1)
        newDataTable.insert(0, "newbs", delcol)
        delcol=newDataTable["longitude"]
        newDataTable=newDataTable.drop("longitude", axis=1)
        newDataTable.insert(1, "longitudeY1", delcol)
        delcol=newDataTable["latitude"]
        newDataTable=newDataTable.drop("latitude", axis=1)
        newDataTable.insert(2, "latitudeX1", delcol)
        #print("Таблица (newDataTable) координат новых базовых станций:")
        #print(newDataTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Подкорректирована таблица c координатами новых базовых станций\n")
        neighbourTable = newDataTable.merge(oldDataTable, how='cross')    
        #print(neighbourTable)
        with open("output.log", "a") as outfile:
            outfile.write("... Объединение таблицы новых базовых станций со старыми базовыми станциями\n")
        x1=neighbourTable["latitudeX1"].astype(float)
        x2=neighbourTable["latitudeX2"].astype(float)
        y1=neighbourTable["longitudeY1"].astype(float)
        y2=neighbourTable["longitudeY2"].astype(float)
        with open("output.log", "a") as outfile:
            outfile.write("... Изменение типа данных координат\n")
        neighbourTable["distance"] = ""
        with open("output.log", "a") as outfile:
            outfile.write("... Добавление столбца distance\n")
        neighbourTable["distance"] = np.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))
        with open("output.log", "a") as outfile:
            outfile.write("... Расчет по формуле расстояние двух базовых станций\n")
        #print(neighbourTable.dtypes)
        #print("Таблица (neighbourTable) с расстоянием двух базовых станций:")
        #print(neighbourTable)
        groupedData = neighbourTable.groupby("newbs")
        minDistance = groupedData["distance"].min()
        #print(minDistance)
        with open("output.log", "a") as outfile:
            outfile.write("... Поиск минимального значению расстоянию\n")
        minDistanceTable = minDistance.reset_index()
        #print(minDistanceTable)
        #newBsTable = pd.merge(minDistanceTable, neighbourTable, left_on='distance', right_on='distance', how='inner')
        #print("Таблица (neighbourTable) новые базовые станции и их соседи:")
        neighbourTable = pd.merge(minDistanceTable, neighbourTable, left_on='distance', right_on='distance', how='inner')
        #print(neighbourTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Загружена в таблицу недостающие данные: LAC и BSC\n")
        #11 объединить таблицы с довесами и новыми базовыми станциями 2g, 4g
        addcol=weekly2gTable["nwName"]
        weekly2gTable.insert(4, "Имя сайта", addcol)
        weekly2gTable["Имя сайта"] = weekly2gTable["Имя сайта"].str[:6]
        addcol=weekly4gTable["cellName"]
        weekly4gTable.insert(3, "Имя сайта", addcol)
        weekly4gTable["Имя сайта"] = weekly4gTable["Имя сайта"].str[:6]        
        #print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки:")
        #print(weekly2gTable)
        #print(weekly4gTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Добавлены в таблицы (weekly2gTable, weekly4gTable) столбцы Имя сайта для соединения с таблицей (neighbourTable)\n")
        #print("Таблицы (newBs2gTable, newBs4gTable) с новыми базовыми станциями 2g, 4g из сайта RDB и еженедельной выгрузки:")
        newBs2gTable = pd.merge(neighbourTable, weekly2gTable, left_on='oldbs', right_on='Имя сайта', how='inner')
        newBs4gTable = pd.merge(neighbourTable, weekly4gTable, left_on='oldbs', right_on='Имя сайта', how='inner')
        #print(newBs2gTable)
        #print(newBs4gTable) 
        with open("output.log", "a") as outfile:
            outfile.write("+ Получены таблицы (newBs2gTable, newBs4gTable ) из объединения таблиц новых базовых станций (neighbourTable) с таблицей из еженедельной выгрузки (weekly2gTable, weekly4gTable)\n")
        #print("Таблицы (oldBs2gTable, oldBs4gTable) с довесами 2g, 4g из сайта CES и еженедельной выгрузки:")
        oldBs2gTable = pd.merge(weekly2gTable, ces2gTable, left_on='nwName', right_on='CELL', how='inner')
        oldBs4gTable = pd.merge(weekly4gTable, ces4gTable, left_on='cellName', right_on='Sector_name', how='inner')
        #print(oldBs2gTable)
        #print(oldBs4gTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Получены таблицы (oldBs2gTable, oldBs4gTable ) из объединения таблиц сайта CES (ces2gTable, ces4gTable) с таблицей из еженедельной выгрузки (weekly2gTable, weekly4gTable)\n")
        print("Таблицы (allBs2gTable, allBs4gTable) с довесами и новыми базовыми станциями 2g, 4g:")
        #allBs2gTable = pd.merge(newBs2gTable, oldBs2gTable, left_on='nwName', right_on='nwName', how='inner')
        #allBs4gTable = pd.merge(newBs4gTable, oldBs4gTable, left_on='cellName', right_on='cellName', how='inner')
        allBs2gTable = pd.concat([newBs2gTable,oldBs2gTable])
        allBs4gTable = pd.concat([newBs4gTable,oldBs4gTable])
        delcol=allBs2gTable["newbs_x"]
        allBs2gTable=allBs2gTable.drop("newbs_x", axis=1)
        delcol=allBs2gTable["newbs_y"]
        allBs2gTable=allBs2gTable.drop("newbs_y", axis=1)
        delcol=allBs2gTable["distance"]
        allBs2gTable=allBs2gTable.drop("distance", axis=1)
        delcol=allBs2gTable["longitudeY1"]
        allBs2gTable=allBs2gTable.drop("longitudeY1", axis=1)
        delcol=allBs2gTable["latitudeX1"]
        allBs2gTable=allBs2gTable.drop("latitudeX1", axis=1)
        delcol=allBs2gTable["longitudeY2"]
        allBs2gTable=allBs2gTable.drop("longitudeY2", axis=1)
        delcol=allBs2gTable["latitudeX2"]
        allBs2gTable=allBs2gTable.drop("latitudeX2", axis=1)
        delcol=allBs2gTable["oldbs"]
        allBs2gTable=allBs2gTable.drop("oldbs", axis=1)
        delcol=allBs2gTable["BS_number"]
        allBs2gTable=allBs2gTable.drop("BS_number", axis=1)
        delcol=allBs2gTable["BS_name"]
        allBs2gTable=allBs2gTable.drop("BS_name", axis=1)
        delcol=allBs2gTable["BS_address"]
        allBs2gTable=allBs2gTable.drop("BS_address", axis=1)
        delcol=allBs2gTable["BSS"]
        allBs2gTable=allBs2gTable.drop("BSS", axis=1)
        delcol=allBs2gTable["BSC"]
        allBs2gTable=allBs2gTable.drop("BSC", axis=1)
        delcol=allBs2gTable["LAC"]
        allBs2gTable=allBs2gTable.drop("LAC", axis=1)
        delcol=allBs2gTable["Reg"]
        allBs2gTable=allBs2gTable.drop("Reg", axis=1)
        delcol=allBs2gTable["CELL"]
        allBs2gTable=allBs2gTable.drop("CELL", axis=1)
        delcol=allBs2gTable["$dn"]
        allBs2gTable=allBs2gTable.drop("$dn", axis=1)
        allBs2gTable.insert(1, "BSC", delcol)
        allBs2gTable["BSC"] = allBs2gTable["BSC"].str[14:20]
        addcol=allBs2gTable["Имя сайта"]
        allBs2gTable.insert(4, "BCF", addcol)
        allBs2gTable["BCF"] = allBs2gTable["BCF"].str[2:6]
        addcol=allBs2gTable["Имя сайта"]
        allBs2gTable.insert(5, "Reg", addcol)
        allBs2gTable["Reg"] = allBs2gTable["Reg"].str[:2]
        allBs2gTable["SW"]="MR10"
        delcol=allBs4gTable["newbs_y"]
        allBs4gTable=allBs4gTable.drop("newbs_y", axis=1)
        delcol=allBs4gTable["distance"]
        allBs4gTable=allBs4gTable.drop("distance", axis=1)
        delcol=allBs4gTable["longitudeY1"]
        allBs4gTable=allBs4gTable.drop("longitudeY1", axis=1)
        delcol=allBs4gTable["latitudeX1"]
        allBs4gTable=allBs4gTable.drop("latitudeX1", axis=1)
        delcol=allBs4gTable["longitudeY2"]
        allBs4gTable=allBs4gTable.drop("longitudeY2", axis=1)
        delcol=allBs4gTable["latitudeX2"]
        allBs4gTable=allBs4gTable.drop("latitudeX2", axis=1)
        delcol=allBs4gTable["pMax"]
        allBs4gTable=allBs4gTable.drop("pMax", axis=1)
        delcol=allBs4gTable["RMOD"]
        allBs4gTable=allBs4gTable.drop("RMOD", axis=1)
        delcol=allBs4gTable["BSS"]
        allBs4gTable=allBs4gTable.drop("BSS", axis=1)
        delcol=allBs4gTable["Reg"]
        allBs4gTable=allBs4gTable.drop("Reg", axis=1)
        delcol=allBs4gTable["newbs_x"]
        allBs4gTable=allBs4gTable.drop("newbs_x", axis=1)
        delcol=allBs4gTable["oldbs"]
        allBs4gTable=allBs4gTable.drop("oldbs", axis=1)
        delcol=allBs4gTable["BSC"]
        allBs4gTable=allBs4gTable.drop("BSC", axis=1)
        delcol=allBs4gTable["LAC"]
        allBs4gTable=allBs4gTable.drop("LAC", axis=1)
        delcol=allBs4gTable["$dn"]
        allBs4gTable=allBs4gTable.drop("$dn", axis=1)
        delcol=allBs4gTable["Имя сайта"]
        allBs4gTable=allBs4gTable.drop("Имя сайта", axis=1)
        delcol=allBs4gTable["Имя сайта_x"]
        allBs4gTable=allBs4gTable.drop("Имя сайта_x", axis=1)
        delcol=allBs4gTable["Имя сайта_y"]
        allBs4gTable=allBs4gTable.drop("Имя сайта_y", axis=1)
        delcol=allBs4gTable["Имя системного модуля"]
        allBs4gTable=allBs4gTable.drop("Имя системного модуля", axis=1)
        delcol=allBs4gTable["Sector_name"]
        allBs4gTable=allBs4gTable.drop("Sector_name", axis=1)
        addcol=allBs4gTable["cellName"]
        allBs4gTable.insert(1, "Reg", addcol)
        allBs4gTable["Reg"] = allBs4gTable["Reg"].str[:2]
        addcol=allBs4gTable["cellName"]
        allBs4gTable.insert(2, "Имя сайта", addcol)
        allBs4gTable["Имя сайта"] = allBs4gTable["Имя сайта"].str[:6]
        print(allBs2gTable)
        print(allBs4gTable)
        with open("output.log", "a") as outfile:
            outfile.write("+ Получены Таблицы (allBs2gTable, allBs4gTable) с довесами и новыми базовыми станциями 2g, 4g\n")
        #12 Добавить файл csv данные, полученные из таблиц.
        allBs2gTable.to_csv('tempfile2g.csv', sep=',', index=False, header=False)
        allBs4gTable.to_csv('tempfile4g.csv', sep=',', index=False, header=False)
        with open("output.log", "a") as outfile:
            outfile.write("+ Добавлены файлы tempfile2g и tempfile4g \n")        
    elif choiceCmd == '2':
        print("+ Выбрано действие - Заполненние данных для БС Ericsson")
        with open("output.log", "a") as outfile:
            outfile.write("+ Выбрано действие - Заполненние данных для БС Ericsson."+"\n")
    else:
        with open("output.log", "a") as outfile:
            outfile.write("- Выбрано действие - Некорректные действия!"+"\n")        
        print("Введите y/n")
    repeat = input("Do you want to continue? (y/n): ")
    if repeat == "n":
        with open("output.log", "a") as outfile:
            outfile.write("+ Завершение программы."+"\n")
        break
    else:
        print("Введите y/n")