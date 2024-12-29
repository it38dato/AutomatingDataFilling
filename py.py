import pandas as pd
import os
import re
import numpy as np

def checkTable(table):
    return table.empty

listCmd = [
    "Заполненние данных для новых сайтов Nokia (1)", 
    "Заполненние данных для новых сайтов Ericsson (2)", 
    "Заполненние данных для довесов Nokia (3)", 
    "Заполненние данных для довесов Ericsson (4)", 
    "Объединить таблицы довесов БС с новыми сайтами (5)"]
locDir = "unloading/"
ces2gTable = pd.DataFrame()
ces4gTable = pd.DataFrame()
weekly2gTable = pd.DataFrame()
weekly4gTable = pd.DataFrame()
oldBs2gTable = pd.DataFrame()
oldBs4gTable = pd.DataFrame()
newBsList = []
prefixs = []
coordList = [] 
dataNewSites = dict()
newDataTable = pd.DataFrame()
oldBsList=[]
oldDataList=[]
dataOldSites = dict()
oldDataTable = pd.DataFrame()
minDistanceTable = pd.DataFrame()
netDir = "data/"
listReg = ["IRK","MGD","SAH","KAM","BRT","VLD"]
bscTemplateDict = {"891018":"BIR067", "28":"IRK028", "120":"IRK120", "396402":"IRK135", "400877":"IRK148", "401257":"IRK169", "401256":"IRK395", "401255":"IRK484", "398493":"KAM070", "912222":"KHB173", "394228":"KHB174", "398471":"MGD069", "324697":"NSK042", "138":"IRK138", "398453":"SAH068", "102":"SAH102", "318":"BRT318", "497":"BRT497", "140":"PRM140", "321":"VLD321", "322":"VLD322"}

#print("+ Создан лог файл output.log")
with open("output.log", "w") as outfile:
    outfile.write("+ Log file created output.log\n")

#1 перечислить список команд, которые может выполнить программа:
print(listCmd)
print("ВНИМАНИЕ! Перед выполнением программы добавьте файлы в папку unloading.") 
choiceCmd = input("Выполните действия: ")

listFiles = os.listdir(locDir)
with open("output.log", "a") as outfile:
    outfile.write("... Checking for files in the folder "+locDir+"\n")   
print("Список загруженных файлов в unloading: ", listFiles)

#13 Замена BSC
#print(bscTemplate)
bscTemplateTable = pd.DataFrame(list(bscTemplateDict.items()), columns=['Key', 'Values'])
print("Таблицa bscTemplateTable с шаблонными данными BSC:")
print(bscTemplateTable)
with open("output.log", "a") as outfile:
    outfile.write("+ Added Tables (allBs2gTable, allBs4gTable) for joining tables newBs2gTable and oldBs2gTable\n")

match choiceCmd:
    case "1":
        #print("+ Выбрано действие - Заполненние данных для БС Nokia")
        with open("output.log", "a") as outfile:
            outfile.write("+ Action selected - Filling in data for Nokia BS\n")

        for file in listFiles:
            #3 Найти незаполненные строки в CES для каждых технологий - 2g, 4g:
            print("...Считываю данные из файла: ", file)
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a file: "+file+"\n")

            if "Table" in file:
                cols = [2, 6, 7, 8, 10, 14, 18]

                print("В файле "+file+" данные из сайта CES")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a CES: "+file+"\n")

                table = pd.read_excel(locDir+"/"+file, usecols=cols)
                table = table[table["BSS"].isna()]
                #print("Таблица (table) 2g, 4g из сайта CES :")
                #print(table)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                if 'CELL' in table:
                    ces2gTable = pd.concat([ces2gTable,table])
                    
                    #14 Добработать программу так, чтобы она корректно считывала данные для базовых станций IO.
                    addcol=ces2gTable["BS_name"]
                    ces2gTable.insert(6, "ifRegIO", addcol)
                    ces2gTable["ifRegIO"] = ces2gTable["ifRegIO"].str[:2]
                    ces2gTable["BS_name"] = ces2gTable["BS_name"].str.replace("^IO", "IR", regex=True)
                    ces2gTable.insert(6, "ifBSnameIO", addcol)
                elif 'Sector_name' in table:
                    ces4gTable = pd.concat([ces4gTable,table])

                    #14 Добработать программу так, чтобы она считывала данные для базовых станций IO.
                    addcol=ces4gTable["Имя сайта"]
                    ces4gTable.insert(6, "ifRegIO", addcol)
                    ces4gTable["ifRegIO"] = ces4gTable["ifRegIO"].str[:2]
                    ces4gTable["Имя сайта"] = ces4gTable["Имя сайта"].str.replace("^IO", "IR", regex=True)
                    ces4gTable.insert(6, "ifBSnameIO", addcol)

                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table with data from the CES\n")
            elif "N_" in file:
                #4 Добавить имееющиеся данные в таблице из еженедельной выгрузки:
                cols = [1, 3, 8, 9]

                print("В файле "+file+" данные из еженедельной выгрузки Nokia")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a Nokia: "+file+"\n")

                table2g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="bts")
                table4g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="lncel")
                #print("Таблица (table2g, table4g) 2g, 4g из еженедельной выгрузки Nokia:")
                #print(table2g)
                #print(table4g)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                weekly2gTable = pd.concat([weekly2gTable,table2g])
                weekly4gTable = pd.concat([weekly4gTable,table4g])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table with data from the Nokia\n")

                #11 объединить таблицы с довесами и новыми базовыми станциями 2g, 4g
                addcol=weekly2gTable["nwName"]
                weekly2gTable.insert(4, "Имя сайта", addcol)
                weekly2gTable["Имя сайта"] = weekly2gTable["Имя сайта"].str[:6]
                addcol=weekly4gTable["cellName"]
                weekly4gTable.insert(4, "Имя сайта", addcol)
                weekly4gTable["Имя сайта"] = weekly4gTable["Имя сайта"].str[:6]

                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrceted a table with data from the Nokia\n")
            elif "Site_" in file:
                #5 Добавить данные координат в таблицу из rdb.:
                print("В файле "+file+" данные из сайта RDB")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a Nokia: "+file+"\n")

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
                            #14 Добработать программу так, чтобы она считывала данные IO.
                            #newBsList.append(bs)
                            #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
                            prefix = bs[:2]
                            #print(prefix)
                            listPrefixs=["IR", "SA", "MD"]

                            if prefix in listPrefixs:
                                newBsList.append(bs)
                                prefixs.append(prefix)
                                prefixs = list(dict.fromkeys(prefixs))
                            #14 Добработать программу так, чтобы она считывала данные IO.
                            elif prefix == "IO":
                                print("... Корректировка префикса:")
                                print(bs)
                                print(prefix)                               
                                bs=bs.replace("IO","IR")
                                prefix=prefix.replace("IO","IR")
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

                cols = ["longitude", "latitude"]        
                newDataTable = pd.DataFrame.from_dict(dataNewSites, orient='index', columns=cols)
                newDataTable = newDataTable.reset_index()
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added Table (newDataTable) with data of new base stations from RDB\n")

                delcol=newDataTable["index"]
                newDataTable=newDataTable.drop("index", axis=1)
                newDataTable.insert(0, "newbs", delcol)
                delcol=newDataTable["longitude"]
                newDataTable=newDataTable.drop("longitude", axis=1)
                newDataTable.insert(1, "longitudeY1", delcol)
                delcol=newDataTable["latitude"]
                newDataTable=newDataTable.drop("latitude", axis=1)
                newDataTable.insert(2, "latitudeX1", delcol)
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected Table (newDataTable) with data of new base stations from RDB\n")
            else:
                continue
        print("Твблица (ces2gTable, ces4gTable) с незаполненными данными 2G, 4G  из CES с учетом IO:")
        print(ces2gTable)
        print(ces4gTable)
        print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки Nokia:")
        print(weekly2gTable)
        print(weekly4gTable)
        print("Список новых базовых станций:")
        print(newBsList)
        print("Список координат станций:")
        print(coordList)
        print("Список новых базовых станций их координат:")
        print(dataNewSites)
        print("Таблица (newDataTable) с координатами новыми базовых станциями из RDB:")
        print(newDataTable)

        #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
        for root, dirs, files in os.walk(netDir):
            lengthDir = len(netDir)
            #with open("output.log", "a") as outfile:
                #    outfile.write("... Checking for files in the folder "+netDir+"\n")
            allDir = root[lengthDir:]
            #print(allDir)

            if ("old" in allDir):
                continue
            elif allDir in listReg:
                #print(allDir)
                for kmlFile in files:
                    #print(kmlFile)
                    if prefixs[0] in kmlFile:
                        #print("Это выгрузка из всех сайтов RDB")
                        #print(kmlFile)  
                        needDir = netDir+allDir+"/"+kmlFile
                        #print(needDir)
                        with open(needDir,"r", encoding="utf8") as rdbFile:
                            file = rdbFile.read()
                        #print(file) 

                        #7 Добавить данные LAC и BSC в таблицу:
                        Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", file, re.DOTALL)
                        for linePlacemark in Placemark:
                            #print(linePlacemark)
                            if ("<longitude>" in linePlacemark) and ("LAC" in linePlacemark) and ("BSC: " in linePlacemark):
                                #print(linePlacemark)
                                if ("<longitude></longitude>" in linePlacemark) and ("<latitude></latitude>" in linePlacemark):
                                    with open("output.txt", "a") as outfile:
                                        outfile.write("- Недостающие данные (Координаты, LAC, BSC)!\n")
                                    continue
                                else:
                                    listBs = re.findall(r"<name>(.*?)</name>", linePlacemark, re.DOTALL)
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

        remainder = (len(oldDataList)//len(oldBsList))
        for numeration in range(len(oldBsList)):
            dataOldSites[oldBsList[numeration]] = [oldDataList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]

        #9 Добавить в пустую таблицу данные из словаря:
        cols = ["longitude", "latitude", "BSC", "LAC"]
        oldDataTable = pd.DataFrame.from_dict(dataOldSites, orient='index', columns=cols)
        oldDataTable = oldDataTable.reset_index()
        with open("output.log", "a") as outfile:
            outfile.write(".+ Added tables of old base stations, their coordinates, LAC and BSC\n")

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
        with open("output.log", "a") as outfile:
            outfile.write(".+ Corrected tables of old base stations, their coordinates, LAC and BSC\n")

        #print("Список старых базовых станций:")
        #print(oldBsList)
        #print("Список координат, LAC И BSC для старых базовых станций:")
        #print(oldDataList)
        #print("Список старых базовых станций, их координат, LAC И BSC:")
        #print(dataOldSites)
        #print("Таблица (oldDataTable) с координатами, LAC И BSC старых базовых станций из Google Earth:")
        #print(oldDataTable)

        neighbourTable = newDataTable.merge(oldDataTable, how='cross')
        with open("output.log", "a") as outfile:
            outfile.write("+ Added a table (neighbourTable) connecting new base stations with old base stations\n")
        
        x1=neighbourTable["latitudeX1"].astype(float)
        x2=neighbourTable["latitudeX2"].astype(float)
        y1=neighbourTable["longitudeY1"].astype(float)
        y2=neighbourTable["longitudeY2"].astype(float)        
        with open("output.log", "a") as outfile:
            outfile.write("... Changing the data type of coordinates\n")

        neighbourTable["distance"] = ""
        neighbourTable["distance"] = np.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))
        with open("output.log", "a") as outfile:
            outfile.write("... Calculation of the distance between two base stations using the formula\n")
        #print(neighbourTable.dtypes)
        #print("Таблица (neighbourTable), соединяющая новые базовые станцит со старыми базовыми станциями:")
        #print(neighbourTable)

        groupedData = neighbourTable.groupby("newbs")
        minDistance = groupedData["distance"].min()
        #print(minDistance)
        with open("output.log", "a") as outfile:
            outfile.write("... Finding the shortest distance\n")

        minDistanceTable = minDistance.reset_index()
        #print(minDistanceTable)
        #newBsTable = pd.merge(minDistanceTable, neighbourTable, left_on='distance', right_on='distance', how='inner')
        #print("Таблица (neighbourTable) новые базовые станции и их соседи:")
        neighbourTable = pd.merge(minDistanceTable, neighbourTable, left_on='distance', right_on='distance', how='inner')
        with open("output.log", "a") as outfile:
            outfile.write("+ The table (neighbourTable) that finds the neighbourhoods of new base stations using the formula has been adjusted\n")
        #print("Таблица (neighbourTable), соединяющая новые базовые станции с соседними станциями по формуле:")
        #print(neighbourTable)

        newBs2gTable = pd.merge(neighbourTable, ces2gTable, left_on='newbs_x', right_on='BS_name', how='inner')
        newBs4gTable = pd.merge(neighbourTable, ces4gTable, left_on='newbs_x', right_on='Имя сайта', how='inner')
        with open("output.log", "a") as outfile:
            outfile.write(".+ Added tables (newBs2gTable, newBs4gTable) adding sector names from CES tables\n")

        #print("Таблицы (newBs2gTable, newBs4gTable) добавляющие название секторов из таблиц CES:")
        #print(newBs2gTable)
        #print(newBs4gTable)

        weekly2gTable=weekly2gTable.drop("nwName", axis=1)
        weekly2gTable=weekly2gTable.drop("$dn", axis=1)
        weekly2gTable=weekly2gTable.drop_duplicates()
        weekly4gTable=weekly4gTable.drop("cellName", axis=1)
        weekly4gTable=weekly4gTable.drop("$dn", axis=1)
        weekly4gTable=weekly4gTable.drop_duplicates()
        with open("output.log", "a") as outfile:
            outfile.write(".+ Corrected tables (weekly2gTable, weekly4gTable)\n")
        #print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки Nokia:")
        #print(weekly2gTable)
        #print(weekly4gTable)

        newBs2gTable = pd.merge(newBs2gTable, weekly2gTable, left_on='oldbs', right_on='Имя сайта', how='inner')
        newBs4gTable = pd.merge(newBs4gTable, weekly4gTable, left_on='oldbs', right_on='Имя сайта', how='inner')
        with open("output.log", "a") as outfile:
            outfile.write(".+ Corrected tables (newBs2gTable, newBs4gTable) adding RAC from weekly uploading tables\n")
        #print("Таблицы (newBs2gTable, newBs4gTable) добавляющие Rac из таблиц еженедельной выгрузки:")
        #print(newBs2gTable)
        #print(newBs4gTable)

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
        print("Таблицы (newBs2gTable, newBs4gTable) добавляющие Rac из таблиц еженедельной выгрузки:")
        print(newBs2gTable)
        print(newBs4gTable)

        #12 Добавить файл csv данные, полученн1ые из таблиц.   
        newBs2gTable.to_csv('newBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
        newBs4gTable.to_csv('newBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
        with open("output.log", "a") as outfile:
            outfile.write("+ Added files to import to the site newBs2gTable и newBs4gTable \n")
    case "2":
        #15 Добавить аналогичным образом данные для технологий Ericsson и довесов:
        print("+ Выбрано действие - Заполненние данных для БС Ericsson")
        with open("output.log", "a") as outfile:
            outfile.write("+ Action selected - Filling in data for Ericsson BS\n")

        for file in listFiles:
            #print("...Считываю данные из файла: ", file)
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a file: "+file+"\n")
            if "Table" in file:
                cols = [2, 6, 7, 8, 10, 14, 18]

                print("В файле "+file+" данные из сайта CES")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a CES: "+file+"\n")

                table = pd.read_excel(locDir+"/"+file, skiprows=1, usecols=cols)
                table = table[table["BSS"].isna()]
                #print("Таблица (table) 2g, 4g из сайта CES :")
                #print(table)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                if 'CELL' in table:
                    ces2gTable = pd.concat([ces2gTable,table])

                     #14 Добработать программу так, чтобы она считывала данные для базовых станций IO.
                    addcol=ces2gTable["CELL"]
                    ces2gTable.insert(1, "Имя сайта", addcol)
                    ces2gTable["Имя сайта"] = ces2gTable["Имя сайта"].str[:6]                   
                elif 'Sector_name' in table:
                    ces4gTable = pd.concat([ces4gTable,table])

                    #14 Добработать программу так, чтобы она считывала данные для базовых станций IO.
                    addcol=ces4gTable["Sector_name"]
                    ces4gTable.insert(1, "Имя сайта", addcol)
                    ces4gTable["Имя сайта"] = ces4gTable["Имя сайта"].str[:6]
            if "Er_" in file:
                #4 Добавить имееющиеся данные в таблице из еженедельной выгрузки:
                cols = [0, 1, 4, 8, 13]

                print("В файле "+file+" данные из еженедельной выгрузки Ericsson")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a Ericsson: "+file+"\n")

                table2g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="GeranCell")
                table4g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="EUtrancellxDD")
                #print("Таблица (table2g, table4g) 2g, 4g из еженедельной выгрузки Ericsson:")
                #print(table2g)
                #print(table4g)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                weekly2gTable = pd.concat([weekly2gTable,table2g])
                weekly4gTable = pd.concat([weekly4gTable,table4g])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table with data from the Ericsson\n")

                #11 объединить таблицы с довесами и новыми базовыми станциями 2g, 4g
                addcol=weekly2gTable["GeranCellId"]
                weekly2gTable.insert(4, "Имя сайта", addcol)
                weekly2gTable["Имя сайта"] = weekly2gTable["Имя сайта"].str[:6]
                addcol=weekly4gTable["NodeId"]
                weekly4gTable.insert(4, "Имя сайта", addcol)
                weekly4gTable["Имя сайта"] = weekly4gTable["Имя сайта"].str[:6]

                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrceted a table with data from the Ericsson\n")
            elif "Site_" in file:
                #5 Добавить данные координат в таблицу из rdb.:
                print("В файле "+file+" данные из сайта RDB")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a Nokia: "+file+"\n")

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
                            #14 Добработать программу так, чтобы она считывала данные IO.
                            #newBsList.append(bs)
                            #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
                            prefix = bs[:2]
                            #print(prefix)
                            listPrefixs=["BU", "VV"]

                            if prefix in listPrefixs:
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

                cols = ["longitude", "latitude"]        
                newDataTable = pd.DataFrame.from_dict(dataNewSites, orient='index', columns=cols)
                newDataTable = newDataTable.reset_index()
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added Table (newDataTable) with data of new base stations from RDB\n")

                delcol=newDataTable["index"]
                newDataTable=newDataTable.drop("index", axis=1)
                newDataTable.insert(0, "newbs", delcol)
                delcol=newDataTable["longitude"]
                newDataTable=newDataTable.drop("longitude", axis=1)
                newDataTable.insert(1, "longitudeY1", delcol)
                delcol=newDataTable["latitude"]
                newDataTable=newDataTable.drop("latitude", axis=1)
                newDataTable.insert(2, "latitudeX1", delcol)
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected Table (newDataTable) with data of new base stations from RDB\n")
            else:
                continue
        #ces2gTable=add2gCes(ces2gTable)
        #ces4gTable=add4gCes(ces4gTable)
        #print("Твблица (ces2gTable, ces4gTable) с незаполненными данными 2G, 4G из CES:")
        #print(ces2gTable)
        #print(ces4gTable)
        #print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки Ericsson:")
        #print(weekly2gTable)
        #print(weekly4gTable)
        #print("Список новых базовых станций:")
        #print(newBsList)
        #print("Список координат станций:")
        #print(coordList)
        #print("Список новых базовых станций их координат:")
        #print(dataNewSites)
        #print("Таблица (newDataTable) с координатами новыми базовых станциями из RDB:")
        #print(newDataTable)

        #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
        for root, dirs, files in os.walk(netDir):
            lengthDir = len(netDir)
            #with open("output.log", "a") as outfile:
                #    outfile.write("... Checking for files in the folder "+netDir+"\n")
            allDir = root[lengthDir:]
            #print(allDir)

            if ("old" in allDir):
                continue
            elif allDir in listReg:
                #print(allDir)
                for kmlFile in files:
                    #print(kmlFile)
                    if prefixs[0] in kmlFile:
                        #print("Это выгрузка из всех сайтов RDB")
                        #print(kmlFile)  
                        needDir = netDir+allDir+"/"+kmlFile
                        #print(needDir)
                        with open(needDir,"r", encoding="utf8") as rdbFile:
                            file = rdbFile.read()
                        #print(file) 

                        #7 Добавить данные LAC и BSC в таблицу:
                        Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", file, re.DOTALL)
                        for linePlacemark in Placemark:
                            #print(linePlacemark)
                            if ("<longitude>" in linePlacemark) and ("LAC" in linePlacemark) and ("BSC: " in linePlacemark):
                                #print(linePlacemark)
                                if ("<longitude></longitude>" in linePlacemark) and ("<latitude></latitude>" in linePlacemark):
                                    with open("output.txt", "a") as outfile:
                                        outfile.write("- Недостающие данные (Координаты, LAC, BSC)!\n")
                                    continue
                                else:
                                    listBs = re.findall(r"<name>(.*?)</name>", linePlacemark, re.DOTALL)
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

        remainder = (len(oldDataList)//len(oldBsList))
        for numeration in range(len(oldBsList)):
            dataOldSites[oldBsList[numeration]] = [oldDataList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]

        #9 Добавить в пустую таблицу данные из словаря:
        cols = ["longitude", "latitude", "BSC", "LAC"]
        oldDataTable = pd.DataFrame.from_dict(dataOldSites, orient='index', columns=cols)
        oldDataTable = oldDataTable.reset_index()
        with open("output.log", "a") as outfile:
            outfile.write(".+ Added tables of old base stations, their coordinates, LAC and BSC\n")

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
        with open("output.log", "a") as outfile:
            outfile.write(".+ Corrected tables of old base stations, their coordinates, LAC and BSC\n")

        #print("Список старых базовых станций:")
        #print(oldBsList)
        #print("Список координат, LAC И BSC для старых базовых станций:")
        #print(oldDataList)
        #print("Список старых базовых станций, их координат, LAC И BSC:")
        #print(dataOldSites)
        #print("Таблица (oldDataTable) с координатами, LAC И BSC старых базовых станций из Google Earth:")
        #print(oldDataTable)

        neighbourTable = newDataTable.merge(oldDataTable, how='cross')
        with open("output.log", "a") as outfile:
            outfile.write("+ Added a table (neighbourTable) connecting new base stations with old base stations\n")
        
        x1=neighbourTable["latitudeX1"].astype(float)
        x2=neighbourTable["latitudeX2"].astype(float)
        y1=neighbourTable["longitudeY1"].astype(float)
        y2=neighbourTable["longitudeY2"].astype(float)        
        with open("output.log", "a") as outfile:
            outfile.write("... Changing the data type of coordinates\n")

        neighbourTable["distance"] = ""
        neighbourTable["distance"] = np.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))
        with open("output.log", "a") as outfile:
            outfile.write("... Calculation of the distance between two base stations using the formula\n")
        #print(neighbourTable.dtypes)
        #print("Таблица (neighbourTable), соединяющая новые базовые станцит со старыми базовыми станциями:")
        #print(neighbourTable)

        groupedData = neighbourTable.groupby("newbs")
        minDistance = groupedData["distance"].min()
        #print(minDistance)
        with open("output.log", "a") as outfile:
            outfile.write("... Finding the shortest distance\n")

        minDistanceTable = minDistance.reset_index()
        #print(minDistanceTable)
        #newBsTable = pd.merge(minDistanceTable, neighbourTable, left_on='distance', right_on='distance', how='inner')
        #print("Таблица (neighbourTable) новые базовые станции и их соседи:")
        neighbourTable = pd.merge(minDistanceTable, neighbourTable, left_on='distance', right_on='distance', how='inner')
        with open("output.log", "a") as outfile:
            outfile.write("+ The table (neighbourTable) that finds the neighbourhoods of new base stations using the formula has been adjusted\n")

        #print("Таблица (neighbourTable), соединяющая новые базовые станции с соседними станциями по формуле:")
        #print(neighbourTable)

        newBs2gTable = pd.merge(neighbourTable, ces2gTable, left_on='newbs_x', right_on='Имя сайта', how='inner')
        newBs4gTable = pd.merge(neighbourTable, ces4gTable, left_on='newbs_x', right_on='Имя сайта', how='inner')
        with open("output.log", "a") as outfile:
            outfile.write(".+ Added tables (newBs2gTable, newBs4gTable) adding sector names from CES tables\n")

        #print("Таблицы (newBs2gTable, newBs4gTable) добавляющие название секторов из таблиц CES:")
        #print(newBs2gTable)
        #print(newBs4gTable)

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

        #12 Добавить файл csv данные, полученн1ые из таблиц.   
        newBs2gTable.to_csv('newBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
        newBs4gTable.to_csv('newBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
        with open("output.log", "a") as outfile:
            outfile.write("+ Added files to import to the site newBs2gTable и newBs4gTable \n")
    case "3":
        #15 Добавить аналогичным образом данные для технологий Ericsson и довесов:
        #print("+ Выбрано действие - Заполненние данных для довесов Nokia")
        with open("output.log", "a") as outfile:
            outfile.write("+ Action selected - Filling in data for Nokia BS\n")
        for file in listFiles:
            #3 Найти незаполненные строки в CES для каждых технологий - 2g, 4g:
            print("...Считываю данные из файла: ", file)
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a file: "+file+"\n")

            if "Table" in file:
                cols = [2, 6, 7, 8, 10, 14, 18]

                print("В файле "+file+" данные из сайта CES")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a CES: "+file+"\n")

                table = pd.read_excel(locDir+"/"+file, usecols=cols)
                table = table[table["BSS"].isna()]
                #print("Таблица (table) 2g, 4g из сайта CES :")
                #print(table)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                if 'CELL' in table:
                    ces2gTable = pd.concat([ces2gTable,table])
                    
                    #14 Добработать программу так, чтобы она корректно считывала данные для базовых станций IO.
                    addcol=ces2gTable["BS_name"]
                    ces2gTable.insert(6, "ifRegIO", addcol)
                    ces2gTable["ifRegIO"] = ces2gTable["ifRegIO"].str[:2]
                    ces2gTable["BS_name"] = ces2gTable["BS_name"].str.replace("^IO", "IR", regex=True)
                    ces2gTable.insert(6, "ifBSnameIO", addcol)
                elif 'Sector_name' in table:
                    ces4gTable = pd.concat([ces4gTable,table])

                    #14 Добработать программу так, чтобы она считывала данные для базовых станций IO.
                    addcol=ces4gTable["Имя сайта"]
                    ces4gTable.insert(6, "ifRegIO", addcol)
                    ces4gTable["ifRegIO"] = ces4gTable["ifRegIO"].str[:2]
                    ces4gTable["Имя сайта"] = ces4gTable["Имя сайта"].str.replace("^IO", "IR", regex=True)
                    ces4gTable.insert(6, "ifBSnameIO", addcol)

                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table with data from the CES\n")
            elif "N_" in file:
                #4 Добавить имееющиеся данные в таблице из еженедельной выгрузки:
                cols = [1, 3, 8, 9]

                print("В файле "+file+" данные из еженедельной выгрузки Nokia")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a Nokia: "+file+"\n")

                table2g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="bts")
                table4g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="lncel")
                #print("Таблица (table2g, table4g) 2g, 4g из еженедельной выгрузки Nokia:")
                #print(table2g)
                #print(table4g)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                weekly2gTable = pd.concat([weekly2gTable,table2g])
                weekly4gTable = pd.concat([weekly4gTable,table4g])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table with data from the Nokia\n")

                #11 объединить таблицы с довесами и новыми базовыми станциями 2g, 4g
                addcol=weekly2gTable["nwName"]
                weekly2gTable.insert(4, "Имя сайта", addcol)
                weekly2gTable["Имя сайта"] = weekly2gTable["Имя сайта"].str[:6]
                addcol=weekly4gTable["cellName"]
                weekly4gTable.insert(4, "Имя сайта", addcol)
                weekly4gTable["Имя сайта"] = weekly4gTable["Имя сайта"].str[:6]

                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrceted a table with data from the Nokia\n")
            else:
                continue
        #print("Твблица (ces2gTable, ces4gTable) с незаполненными данными 2G, 4G  из CES с учетом IO:")
        #print(ces2gTable)
        #print(ces4gTable)
        #print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки Nokia:")
        #print(weekly2gTable)
        #print(weekly4gTable)

        #print(checkTable(ces2gTable))
        #print(checkTable(ces4gTable))
        if checkTable(ces4gTable)==True:
            print("Можно заполнять 2G")
            oldBs2gTable = pd.merge(weekly2gTable, ces2gTable, left_on='Имя сайта', right_on='ifBSnameIO', how='inner')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added tables (oldBs2gTable) with completed site\n")

            print("работа в процессе (Нужно скорректировать код для заполнения данных 2G)")
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrected the Table (oldBs2gTable)\n")

            oldBs2gTable.to_csv('oldBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added files to import to the site oldBs2gTable \n")
        elif checkTable(ces2gTable)==True:
            print("Можно заполнять 4G")
            oldBs4gTable = pd.merge(ces4gTable, weekly4gTable, left_on='Имя сайта', right_on='Имя сайта', how='inner')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added tables (oldBs4gTable) with completed site\n")
            
            oldBs4gTable=oldBs4gTable.drop("BSS", axis=1)
            oldBs4gTable=oldBs4gTable.drop("Reg", axis=1)
            oldBs4gTable=oldBs4gTable.drop("Имя сайта", axis=1)
            oldBs4gTable=oldBs4gTable.drop("RMOD", axis=1)
            oldBs4gTable=oldBs4gTable.drop("ifBSnameIO", axis=1)
            oldBs4gTable=oldBs4gTable.drop("EXT_port_on_System_module", axis=1)
            oldBs4gTable=oldBs4gTable.drop("$dn", axis=1)
            oldBs4gTable=oldBs4gTable.drop("cellName", axis=1)
            oldBs4gTable=oldBs4gTable.drop("pMax", axis=1)
            oldBs4gTable = oldBs4gTable.drop_duplicates()
            oldBs4gTable = oldBs4gTable.reindex(columns=["ifRegIO", "Имя системного модуля", "Sector_name", "tac"])
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrected the Table (oldBs4gTable)\n")

            oldBs4gTable.to_csv('oldBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added files to import to the site oldBs4gTable \n")
        else:
            print("- Некорректное заполнение данных в таблицах.")
            with open("output.log", "a") as outfile:
                outfile.write("- Incorrect filling of data in tables.\n")

        print("Таблицы (oldBs2gTable, oldBs4gTable) с довесами (Новых сайтов тут быть не должно):")
        print(oldBs2gTable)
        print(oldBs4gTable)
    case "4":
        #15 Добавить аналогичным образом данные для технологий Ericsson и довесов:
        #print("+ Выбрано действие - Заполненние данных для довесов Ericsson")
        with open("output.log", "a") as outfile:
            outfile.write("+ Action selected - Filling in data for Ericsson BS\n")

        for file in listFiles:
            #print("...Считываю данные из файла: ", file)
            with open("output.log", "a") as outfile:
                outfile.write("... Reading data from a file: "+file+"\n")
            if "Table" in file:
                cols = [2, 6, 7, 8, 10, 14, 18]

                print("В файле "+file+" данные из сайта CES")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a CES: "+file+"\n")

                table = pd.read_excel(locDir+"/"+file, skiprows=1, usecols=cols)
                table = table[table["BSS"].isna()]
                #print("Таблица (table) 2g, 4g из сайта CES :")
                #print(table)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                if 'CELL' in table:
                    ces2gTable = pd.concat([ces2gTable,table])

                     #14 Добработать программу так, чтобы она считывала данные для базовых станций IO.
                    addcol=ces2gTable["CELL"]
                    ces2gTable.insert(1, "Имя сайта", addcol)
                    ces2gTable["Имя сайта"] = ces2gTable["Имя сайта"].str[:6]                   
                elif 'Sector_name' in table:
                    ces4gTable = pd.concat([ces4gTable,table])

                    #14 Добработать программу так, чтобы она считывала данные для базовых станций IO.
                    addcol=ces4gTable["Sector_name"]
                    ces4gTable.insert(1, "Имя сайта", addcol)
                    ces4gTable["Имя сайта"] = ces4gTable["Имя сайта"].str[:6]
            if "Er_" in file:
                #4 Добавить имееющиеся данные в таблице из еженедельной выгрузки:
                cols = [0, 1, 4, 8, 13]

                print("В файле "+file+" данные из еженедельной выгрузки Ericsson")
                with open("output.log", "a") as outfile:
                    outfile.write("... Reading data from a Ericsson: "+file+"\n")

                table2g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="GeranCell")
                table4g = pd.read_excel(locDir+"/"+file, usecols=cols, sheet_name="EUtrancellxDD")
                #print("Таблица (table2g, table4g) 2g, 4g из еженедельной выгрузки Ericsson:")
                #print(table2g)
                #print(table4g)
                with open("output.log", "a") as outfile:
                    outfile.write("+ File contents received "+file+"\n")

                weekly2gTable = pd.concat([weekly2gTable,table2g])
                weekly4gTable = pd.concat([weekly4gTable,table4g])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added a table with data from the Ericsson\n")

                #11 объединить таблицы с довесами и новыми базовыми станциями 2g, 4g
                addcol=weekly2gTable["GeranCellId"]
                weekly2gTable.insert(4, "Имя сайта", addcol)
                weekly2gTable["Имя сайта"] = weekly2gTable["Имя сайта"].str[:6]
                addcol=weekly4gTable["NodeId"]
                weekly4gTable.insert(4, "Имя сайта", addcol)
                weekly4gTable["Имя сайта"] = weekly4gTable["Имя сайта"].str[:6]

                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrceted a table with data from the Ericsson\n")
            else:
                continue
        #ces2gTable=add2gCes(ces2gTable)
        #ces4gTable=add4gCes(ces4gTable)
        print("Твблица (ces2gTable, ces4gTable) с незаполненными данными 2G, 4G из CES:")
        print(ces2gTable)
        print(ces4gTable)
        print("Таблицы (weekly2gTable, weekly4gTable) 2g, 4g из еженедельной выгрузки Ericsson:")
        print(weekly2gTable)
        print(weekly4gTable)
    
        oldBs2gTable = pd.merge(weekly2gTable, ces2gTable, left_on='Имя сайта', right_on='Имя сайта', how='inner')
        oldBs4gTable = pd.merge(weekly4gTable, ces4gTable, left_on='Имя сайта', right_on='Имя сайта', how='inner')
        with open("output.log", "a") as outfile:
            outfile.write("+ Added tables (oldBs2gTable, oldBs4gTable) with completed site\n")    

        #print("Таблицы (oldBs2gTable, oldBs4gTable) с довесами (Новых сайтов тут быть не должно):")       
        #print(oldBs2gTable)
        #print(oldBs4gTable)

        #print(checkTable(ces2gTable))
        #print(checkTable(ces4gTable))

        if checkTable(ces4gTable)==True:
            oldBs2gTable = pd.merge(weekly2gTable, ces2gTable, left_on='Имя сайта', right_on='ifBSnameIO', how='inner')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added tables (oldBs2gTable) with completed site\n")

            print("будет доработка кода для 2g.")
            oldBs2gTable = oldBs2gTable.reindex(columns=["Reg", "BS_name", "Values", "TG", "Имя сайта", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "CELL"])
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrected the Table (oldBs2gTable, oldBs4gTable)\n")

            oldBs2gTable.to_csv('oldBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added files to import to the site oldBs2gTable \n")
        elif checkTable(ces2gTable)==True:
            oldBs4gTable = pd.merge(ces4gTable, weekly4gTable, left_on='Имя сайта', right_on='Имя сайта', how='inner')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added tables (oldBs2gTable, oldBs4gTable) with completed site\n")

            oldBs4gTable=oldBs4gTable.drop("BSS", axis=1)
            oldBs4gTable=oldBs4gTable.drop("Имя сайта", axis=1)
            oldBs4gTable=oldBs4gTable.drop("Subreg", axis=1)
            oldBs4gTable=oldBs4gTable.drop("LTE_Frequency", axis=1)
            oldBs4gTable=oldBs4gTable.drop("RRUS", axis=1)
            oldBs4gTable=oldBs4gTable.drop("NodeId", axis=1)
            oldBs4gTable=oldBs4gTable.drop("EUtranCellTDDId", axis=1)
            oldBs4gTable=oldBs4gTable.drop("cellBarred", axis=1)
            oldBs4gTable=oldBs4gTable.drop("dlConfigurableFrequencyStart", axis=1)
            oldBs4gTable = oldBs4gTable.drop_duplicates()
            oldBs4gTable = oldBs4gTable.reindex(columns=["Reg", "System_module_name_4G", "tac", "Sector_name"])
            with open("output.log", "a") as outfile:
                outfile.write("+ Corrected the Table (oldBs4gTable)\n")

            oldBs4gTable.to_csv('oldBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added files to import to the site oldBs4gTable \n")
        elif checkTable(ces2gTable)==False and checkTable(ces4gTable)==False:
            oldBs2gTable = pd.merge(ces2gTable, weekly2gTable, left_on='Имя сайта', right_on='Имя сайта', how='inner')
            oldBs4gTable = pd.merge(ces4gTable, weekly4gTable, left_on='Имя сайта', right_on='Имя сайта', how='inner')
            with open("output.log", "a") as outfile:
                outfile.write("+ Added tables (oldBs2gTable, oldBs4gTable) with completed site\n")

            #print(checkTable(oldBs2gTable))
            #print(checkTable(oldBs4gTable))

            if checkTable(oldBs2gTable)==True:
                oldBs4gTable=oldBs4gTable.drop("BSS", axis=1)
                oldBs4gTable=oldBs4gTable.drop("Имя сайта", axis=1)
                oldBs4gTable=oldBs4gTable.drop("Subreg", axis=1)
                oldBs4gTable=oldBs4gTable.drop("LTE_Frequency", axis=1)
                oldBs4gTable=oldBs4gTable.drop("RRUS", axis=1)
                oldBs4gTable=oldBs4gTable.drop("NodeId", axis=1)
                oldBs4gTable=oldBs4gTable.drop("EUtranCellTDDId", axis=1)
                oldBs4gTable=oldBs4gTable.drop("cellBarred", axis=1)
                oldBs4gTable=oldBs4gTable.drop("dlConfigurableFrequencyStart", axis=1)
                oldBs4gTable = oldBs4gTable.drop_duplicates()
                oldBs4gTable = oldBs4gTable.reindex(columns=["Reg", "System_module_name_4G", "tac", "Sector_name"])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected the Table (oldBs4gTable)\n")

                oldBs4gTable.to_csv('oldBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added files to import to the site oldBs2gTable, oldBs4gTable \n")
            else:
                print("будет доработка кода для 2g.")
                oldBs4gTable=oldBs4gTable.drop("BSS", axis=1)
                oldBs4gTable=oldBs4gTable.drop("Имя сайта", axis=1)
                oldBs4gTable=oldBs4gTable.drop("Subreg", axis=1)
                oldBs4gTable=oldBs4gTable.drop("LTE_Frequency", axis=1)
                oldBs4gTable=oldBs4gTable.drop("RRUS", axis=1)
                oldBs4gTable=oldBs4gTable.drop("NodeId", axis=1)
                oldBs4gTable=oldBs4gTable.drop("EUtranCellTDDId", axis=1)
                oldBs4gTable=oldBs4gTable.drop("cellBarred", axis=1)
                oldBs4gTable=oldBs4gTable.drop("dlConfigurableFrequencyStart", axis=1)
                oldBs4gTable = oldBs4gTable.drop_duplicates()
                oldBs2gTable = oldBs2gTable.reindex(columns=["Reg", "BS_name", "Values", "TG", "Имя сайта", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "CELL"])
                oldBs4gTable = oldBs4gTable.reindex(columns=["Reg", "System_module_name_4G", "LAC", "Sector_name"])
                with open("output.log", "a") as outfile:
                    outfile.write("+ Corrected the Table (oldBs2gTable, oldBs4gTable)\n")

                oldBs4gTable.to_csv('oldBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
                with open("output.log", "a") as outfile:
                    outfile.write("+ Added files to import to the site oldBs2gTable, oldBs4gTable \n")
        else:
            print("- Некорректное заполнение данных в таблицах.")
            with open("output.log", "a") as outfile:
                outfile.write("- Incorrect filling of data in tables.\n")
        print("Таблицы (oldBs2gTable, oldBs4gTable) с довесами (Новых сайтов тут быть не должно):")
        print(oldBs2gTable)
        print(oldBs4gTable)
    case "5":
        #15 Добавить аналогичным образом данные для технологий Ericsson и довесов:
        #print("+ Выбрано действие - Объединить таблицы довесов БС с новыми сайтамиС")
        with open("output.log", "a") as outfile:
            outfile.write("+ Action selected - Filling in data for ALL sites BS\n")

        print("Таблицы (oldBs2gTable, oldBs4gTable) с довесами (Новых сайтов тут быть не должно):")
        print(oldBs2gTable)
        print(oldBs4gTable)
        print("Таблицы (newBs2gTable, newBs4gTable) с новыми сайтами:")
        print(newBs2gTable)
        print(newBs4gTable)

        allBs2gTable = pd.concat([newBs2gTable,oldBs2gTable])
        allBs4gTable = pd.concat([newBs4gTable,oldBs4gTable])
        with open("output.log", "a") as outfile:
            outfile.write("+ Added the Table (allBs2gTable, allBs4gTable) for all sites\n")
        #print("Таблицы (allBs2gTable, allBs4gTable) с довесами и новыми сайтамиg:")
        #print(allBs2gTable)
        #print(allBs4gTable)

        #12 Добавить файл csv данные, полученн1ые из таблиц.   
        allBs2gTable.to_csv('allBs2gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
        allBs4gTable.to_csv('allBs4gTable.csv', sep=';', index=False, header=False, encoding='UTF-8-SIG')
        with open("output.log", "a") as outfile:
            outfile.write("+ Added files to import to the site tempfile2g и tempfile4g \n")
    case _:
        print("- Выбрано действие - Некорректные действия!")
        with open("output.log", "a") as outfile:
            outfile.write("-  Action selected - Incorrect actions!\n")