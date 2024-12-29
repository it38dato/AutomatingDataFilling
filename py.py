import pandas as pd
import os
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
        print("ВНИМАНИЕ! Выгрузите таблицу с незаполненными данными из CES и поместите файл в папку unloading, также добавьте файл еженедельной выгрузки!")    
        path = "unloading/"
        #files = [file for file in os.listdir(path) if not file.startswith('.')]
        listfiles = os.listdir(path)
        print("Список загруженных файлов: ", listfiles)
        ces2g = pd.DataFrame()
        ces4g = pd.DataFrame()
        unloading2g = pd.DataFrame()
        unloading4g = pd.DataFrame()
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
        print(tableBs2g)
        print(tableBs4g)
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