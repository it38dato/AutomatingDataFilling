import pandas as pd
import os
import re
#1 перечислить список команд, которые может выполнить программа:
repeat="y"
with open("output.txt", "w") as outfile:
    outfile.write("") 
while repeat == "y":
    print("Выполните действия, которые необходимо выполнить в CES:")
    listcmd=['Заполненние данных для БС Nokia (1)', 'Заполненние данных для БС Ericsson (2)']
    print(listcmd)
    choicecmd = input()
    #print(choicecmd)
    if choicecmd == '1':
        #print("Выполняю Заполненние данных для БС Nokia")
        #with open("output.txt", "a") as outfile:
        #    outfile.write("Выполняю Заполненние данных для БС Nokia"+"\n")
        #2 Собрать в список данные, которые необходимо заполнить в шаблоне: 
        listtemplate=["Reg","CELL","SW",'BSC','BCF','LAC','RAC2g','Имя сайта','Sector_name','RAC3g','URA','RNC_ID']
        print("Для заполнения нужны следующие данные: ", listtemplate)
        #with open("output.txt", "a") as outfile:
        #    outfile.write("Для заполнения нужны следующие данные: "+listtemplate[0]+","+listtemplate[1]+","+listtemplate[2]+","+listtemplate[3]+","+listtemplate[4]+","+listtemplate[5]+","+listtemplate[6]+","+listtemplate[7]+","+listtemplate[8]+","+listtemplate[9]+","+listtemplate[10]+","+listtemplate[11]+"\n")
        #3 Найти незаполненные строки БС IR2468 в таблице из CES для каждых технологий - 2g, 4g:
        print("ВНИМАНИЕ! Выгрузите таблицу с незаполненными данными из еженедельной выгрузки, из сайтов CES и RDB и поместите файл в папку unloading.")    
        path = "unloading/"
        #files = [file for file in os.listdir(path) if not file.startswith('.')]
        listfiles = os.listdir(path)
        print("Список загруженных файлов: ", listfiles)
        ces2g = pd.DataFrame()
        ces4g = pd.DataFrame()
        unloading2g = pd.DataFrame()
        unloading4g = pd.DataFrame()
        newbslist=[]
        coordlist=[]
        prefixs=[]
        oldbslist=[]
        olddatalist=[]
        datasites = dict()
        dataloldsites = dict()
        for file in listfiles:
            print("Считываю данные из файла: ", file)
            #4 Добавить имееющиеся данные в таблице из еженедельной выгрузки:
            if "N_" in file:
                #print("Это еженедельная выгрузка из Nokia")
                cols = [3, 8, 9]
                table2g = pd.read_excel(path+"/"+file, usecols=cols, sheet_name='bts')
                table4g = pd.read_excel(path+"/"+file, usecols=cols, sheet_name='lncel')
                print("Корректирую таблицы")
                delcol=table2g["nwName"]
                table2g=table2g.drop("nwName", axis=1)
                table2g.insert(1, "Sector_name", delcol)
                delcol=table2g["locationAreaIdLAC"]
                table2g=table2g.drop("locationAreaIdLAC", axis=1)
                table2g.insert(2, "LAC", delcol)
                delcol=table2g["Sector_name"]
                table2g.insert(3, "BCF", delcol)
                table2g["BCF"] = table2g["BCF"].str[2:6]
                delcol=table4g["cellName"]
                table4g=table4g.drop("cellName", axis=1)
                table4g.insert(1, "Sector_name", delcol)
                delcol=table4g["tac"]
                table4g=table4g.drop("tac", axis=1)
                table4g.insert(2, "LAC", delcol)
                table4g = table4g.drop("pMax", axis=1)
                #print(table2g)
                #print(table4g)
                unloading2g = pd.concat([unloading2g,table2g]) 
                unloading4g = pd.concat([unloading4g,table4g]) 
                print("Успешно прочитал данные из файла: ", file)
            #5 Добавить данные координат в таблицу из rdb.:
            elif "Site_" in file:
                #print("Это выгрузка из сайта RDB")
                with open(path+"/"+file,"r", encoding="utf8") as rdbfile:
                    inputfile = rdbfile.read()
                print("Корректирую данные из файла")
                #print(inputfile)
                Placemark = re.findall(r'<Placemark>(.*?)</Placemark>', inputfile, re.DOTALL)
                for i in Placemark:
                    #print(i)
                    listbs = re.findall(r'<name>(.*?)</name>', i, re.DOTALL)
                    #print(listbs)
                    for bs in listbs:
                        if '/' in bs:
                            bs = bs.split('/')[0]
                            i1 = 2
                            i2 = 3
                            bs = bs[:i1] + bs[i2+1:]
                            newbslist.append(bs)
                            #print(newbslist)                       
                            #print(bs)
                            #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
                            prefix = bs[:2]
                            prefixs.append(prefix)
                            prefixs = list(dict.fromkeys(prefixs))
                            #print(prefix)
                        else:
                            print("Имя базой станции другого формата!")
                coordinates = re.findall(r'<coordinates>(.*?)</coordinates>', i, re.DOTALL)
                #print(coordinates)
                for coords in coordinates:
                    #print(coords)
                    longitude = coords.split(',')[0]
                    latitude = coords.split(',')[1]
                    #print(longitude + " " + latitude + "\n")
                    coordlist.append(longitude)
                    coordlist.append(latitude)
                print("Успешно прочитал данные из файла: ", file)
            else:
                #print("Это выгрузка из сайта CES")
                print("Корректирую таблицы")
                cols = [2, 6, 7, 8, 10, 14]
                table = pd.read_excel(path+"/"+file, usecols=cols)
                table = table[table["BSS"].isna()]
                #print(table)
                if "BS_address" in table:
                    table2g=table.drop("BS_number", axis=1)
                    table2g=table2g.drop("BS_address", axis=1)
                    delcol=table2g["BS_name"]
                    table2g=table2g.drop("BS_name", axis=1)
                    table2g.insert(2, "Имя сайта", delcol)
                    delcol=table2g["CELL"]
                    table2g=table2g.drop("CELL", axis=1)
                    table2g.insert(2, "Sector_name", delcol)
                    table2g=table2g.drop("BSS", axis=1)
                    #print(table2g)
                    ces2g = pd.concat([ces2g,table2g])
                elif "RMOD" in table: 
                    table4g=table.drop("Имя системного модуля", axis=1)
                    table4g=table4g.drop("RMOD", axis=1)
                    table4g=table4g.drop("BSS", axis=1)
                    #print(table4g)
                    ces4g = pd.concat([ces4g,table4g])
                else: 
                    print("unknow table")
                #print(table)
                print("Успешно прочитал данные из файла: ", file)
        #print(unloading2g)
        #print(unloading4g)
        #print(ces2g)
        #print(ces4g)
        print("Получил таблицы 2g, 4g")
        tableBs2g = pd.merge(unloading2g, ces2g, left_on='Sector_name', right_on='Sector_name', how='inner')
        tableBs4g = pd.merge(unloading4g, ces4g, left_on='Sector_name', right_on='Sector_name', how='inner')
        #print(tableBs2g)
        #print(tableBs4g)
        print("Корректирую данные из файла")
        print(newbslist)
        #print(" - вывожу Список базовых станций")
        print(coordlist)
        #print(" - вывожу Список координат")
        remainder = (len(coordlist)//len(newbslist))
        #print(remainder)
        for numeration in range(len(newbslist)):
            #print(numeration)
            datasites[newbslist[numeration]] = [coordlist[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
        print(datasites)
        print(" - Добавляю словарь с названиями базовых станций и координатами.")
        cols = ["longitude", "latitude"]
        rdbfile2g = pd.DataFrame()
        rdbfile2g = pd.DataFrame.from_dict(datasites, orient='index', columns=cols)
        rdbfile2g = rdbfile2g.reset_index()
        print(rdbfile2g)
        #6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
        netpath = "data/"
        print("Корректирую данные из rdb")
        lengthdir=len(netpath)
        listreg=["IRK","MGD","SAH","KHA","KAM"]
        for root, dirs, files in os.walk(netpath):
            alldir = root[lengthdir:]
            #print(alldir) 
            if ("old" in alldir):
                #print("FALSE")
                continue
            elif alldir in listreg:
                #print(alldir)
                for kmlfile in files:
                    #print(kmlfile)
                    if prefixs[0] in kmlfile:
                        #print("Это выгрузка из всех сайтов RDB")
                        print("Считываю данные из файла: ", kmlfile)
                        #print(kmlfile)                        
                        needdir = netpath+alldir+"/"+kmlfile
                        #print(needdir)
                        #with open(kmlfile,"r", encoding="utf8") as rdbfile:
                        with open(needdir,"r", encoding="utf8") as rdbfile:
                            file = rdbfile.read()
                        #print(file) 
                        #7 Добавить данные LAC и BSC в таблицу:
                        print("Корректирую данные из rdb файлов:")
                        Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", file, re.DOTALL)
                        for i in Placemark:
                            #print(i)
                            if ("<longitude>" in i) and ("LAC" in i) and ("BSC: " in i):
                                #print(i)
                                if ("<longitude></longitude>" in i) and ("<latitude></latitude>" in i):
                                    #print(" - избавляюсь от незаполненных координат для БС")
                                    #with open("output.txt", "a") as outfile:
                                    #    outfile.write("Недостающие данные (Координаты, Lac, SC)!\n")
                                    continue
                                else:
                                    listbs = re.findall(r"<name>(.*?)</name>", i, re.DOTALL)
                                    #print(" - проверяю корректность заполнения названий БС")
                                    for bs in listbs:
                                        if (len(bs)==6) == True:
                                            #print(bs)
                                            with open("output.txt", "a") as outfile:
                                                outfile.write(bs+"\n")
                                            oldbslist.append(bs)
                                            #print(" - Добавляю в Список название")
                                        else:
                                            with open("output.txt", "a") as outfile:
                                                outfile.write("Имя базой станции "+ bs +" некорректного формата!\n")
                                            continue
                                    listcoords = re.findall(r"<longitude>(.*?)</latitude>", i, re.DOTALL)
                                    #print(" - проверяю корректность заполнения координат")
                                    for coords in listcoords:
                                        #print(coords)
                                        coordinates = coords.split("</longitude>\n     <latitude>")
                                        #print(coordinates)
                                        longitude = coordinates[0]
                                        latitude = coordinates[1]
                                        #print(longitude + " " + latitude + "\n")
                                        #print(" - корректирую заполнение координат")
                                        with open("output.txt", "a") as outfile:
                                            outfile.write(longitude + " " + latitude + "\n")
                                        olddatalist.append(longitude)
                                        olddatalist.append(latitude)
                                        #print(" - Добавляю в Список коорднат")
                                    listbsctac = re.findall(r"<description>BSC: (.*?)</description>", i, re.DOTALL)
                                    #print(" - проверяю корректность заполнения LAC и BSC")
                                    #print(listbsctac)
                                    for bsctac in listbsctac:
                                        #print(bsctac)
                                        data = bsctac.split(" LAC: ")
                                        #print(data)
                                        bsc = data[0]
                                        lac = data[1]
                                        #print(bsc + " " + lac + "\n")
                                        #print(" - корректирую заполнение LAC и BSC")
                                        with open("output.txt", "a") as outfile:
                                            outfile.write(bsc + " " + lac + "\n")
                                        olddatalist.append(bsc)
                                        olddatalist.append(lac)
                                        #print(" - Добавляю в Список LAC и BSC")
                            elif ("<longitude>" in i) and ("LAC" in i) and ("URA: " in i):
                                #print("ВОЗМОЖНО, эти данные понадобятся для заполнения 3g!")
                                #print(i)
                                continue
                            else:
                                #print("Недостающие данные (Координаты, Lac, BSC)")
                                #with open("output.txt", "a") as outfile:
                                #    outfile.write("Недостающие данные (Координаты, Lac, BSC)!\n")
                                #break
                                continue
                        #print(oldbslist)
                        #print(" - Список название БС")
                        #print(olddatalist)
                        #print(" - Список коорднат, Lac, BSC")
            else:
                #print("TRUE")
                continue
        #8 Добавить в пустой словарь название БС, координаты, LAC И BSC:
        #print(oldbslist)
        #print(olddatalist)
        remainder = (len(olddatalist)//len(oldbslist))
        for numeration in range(len(oldbslist)):
            #print(numeration)
            dataloldsites[oldbslist[numeration]] = [olddatalist[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
        #print(dataloldsites)
        print(" - Добавляю словарь с названиями соседних базовых станций и координатами, LAC И BSC.")
    elif choicecmd == '2':
        print("Ты выбрал Заполненние данных для БС Ericsson")
        with open("output.txt", "a") as outfile:
            outfile.write("Ты выбрал Заполненние данных для БС Ericsson"+"\n")
    else:
        print("Введите y/n")        
    repeat = input("Do you want to continue? (y/n): ")
    if repeat == "n":
        break
    else:
        print("Введите y/n")