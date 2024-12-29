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
        print("Ты выбрал Заполненние данных для БС Nokia")
        with open("output.txt", "a") as outfile:
            outfile.write("Ты выбрал Заполненние данных для БС Nokia"+"\n")
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