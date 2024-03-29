import csv
from random import choice
import datetime
# from csv import writer
from tempfile import NamedTemporaryFile
import shutil
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)
basic_csv = 'basic.csv' # csv of word
time_csv = 'time.csv' # csv of time

def my_append(id_0,questionToday_list,temp): # append random word in questionToday_list
    while temp != 0:
        no_random = choice(id_0)
        questionToday_list.append(no_random)
        id_0.remove(no_random)
        temp -= 1
    return questionToday_list
def check(file_csv,number,id_0,questionToday_list): # check for new word or old word
    id_0 = []
    with open(file_csv) as f:
        reader = csv.reader(f)    
        temp = int(0)
        if number == '0':
            for row in reader:
                if row[3] == number:
                    id_0.append([row[0],row[1],row[2],row[3],'on']) 
            temp = int(input('how much you want new words? : '))
            if temp > len(id_0):
                temp = len(id_0)
                print('all new words in csv is %i' % temp)
        elif number == 'another':
            for row in reader:
                if row[3] != '0' and row[3] != '1' and row[3] != '3' and row[3] != '7' and row[3] != '15' and row[3] != '30' and row[3] != '31':
                    list_another.append([row[0],row[1],row[2],row[3],row[4]])
        else:
            for row in reader:
                if row[3] == number:
                    id_0.append([row[0],row[1],row[2],row[3],'on'])
            temp = len(id_0)
    questionToday_list = my_append(id_0,questionToday_list,temp)

def check_again(file_csv,number,questionToday_list): # check again for new word or old word
    id_0 = []
    with open(file_csv) as f:
        reader = csv.reader(f)    
        temp = int(0)
        if number == '0':
            for row in reader:
                if row[3] == number and row[4] == 'on':
                    questionToday_list.append([row[0],row[1],row[2],row[3],row[4]]) 
        else:
            for row in reader:
                if row[3] == number and row[4] == 'on':
                    questionToday_list.append([row[0],row[1],row[2],row[3],row[4]])
    return questionToday_list

def last_id(): # give the last id
    n = int(0)
    with open(basic_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            n = int(row[0])
        return n
def append_list_as_row(file_csv,list_of_elem): # send new word in csv
    # Open file in append mode
    with open(file_csv, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        # List of strings
        
def edit_csv(filename,line0,line1,line2,line3,line4): # edit csv for basic.csv
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            if line0 == row[0]:
                row[0],row[1],row[2],row[3],row[4] = line0 ,line1 ,line2 ,line3 ,line4
                
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
    
def edit_time_csv(filename,line0,line1,line2): # edit csv for time.csv
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            row[0],row[1],row[2] = line0 ,line1 ,line2
            writer.writerow(row)

    shutil.move(tempfile.name, filename)    

def leitner(questionToday_list): # question words
    sure = 'null'
    for item in questionToday_list:
        if item[4] == 'on':
            print(item[1])
            engine.say(item[1])
            engine.runAndWait()
            temp = input(' you want continue? (y/n): ')
            
            if temp == 'n' or temp == 'N':
                sure = input('are you sure? (y/n): ')
                if sure == 'n' or sure == 'N':
                    temp = 'y' # TODO
                elif sure == 'y' or sure == 'Y' or sure == '':
                    print('leitner is off!')
                    break
                
            if temp == 'y' or temp == 'Y' or temp == '':
                print('[%s] mishavad [%s]' % (item[1] , item[2]))
                javab = input('your hads is true? (y/n): ')
                if javab == 'n' or javab == 'N':
                    item[3] , item[4] = '1' , 'off'
                elif javab == 'y' or javab == 'Y' or javab == '':
                    item[3] , item[4] = str(int(item[3]) + 1) , 'off'
    return sure
    # for row in questionToday_list: # TODO
    #     edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])

def show():
    show_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    with open(basic_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            show_list[int(row[3])] += 1
        for i in range(len(show_list)):
            if show_list[i] != 0:
                print('value words [%s] day house is [%i]' % (i,show_list[i]))

with open(basic_csv) as f:
    reader = csv.reader(f)
    id_0 = list() # list Ids in CSV
    questionToday_list = list() # list word of question day
    list_another = list() # list word of does't question day
    while True:    
        init = input('do you want? (leitner[l]/input word in app[i]/show status[s]/off the app[o]): ')
        
        if init == 'o' or init == 'O': # off the app
            print('app is off')
            break
        
        elif init == 's' or init == 'S': # show value words in all days house
            show()
        
        elif init == 'i' or init == 'I': # send word in app
            print('warning!!! ,all new words insert to one day house')
            new_word = int(0) # TODO
            while True:
                word = input('give me the word: ')
                word_translate = input('give me the word translation: ')
                append_list_as_row(basic_csv,[str(last_id() +1),word.strip(),word_translate.strip(),'1','off'])
                # Append a list as new line to an old csv file
                new_word +=1
                print('done! you insert %i word in leitner' % new_word)
                temp = input('you want to continue? (y/n): ')
                if temp == 'n' or temp == 'N':
                    break
                
        elif init == 'l' or init == 'L' or init == '': # leitner
            questionToday_list = []
            with open(time_csv) as time_tomorrow:
                reader = csv.reader(time_tomorrow)
                for row in reader:
                    tomorrow_year , tomorrow_month , tomorrow_day = int(row[0]) , int(row[1]) , int(row[2])
                e = datetime.datetime.now()
                if e.year > tomorrow_year or (e.year == tomorrow_year and e.month > tomorrow_month) or (e.year == tomorrow_year and e.month == tomorrow_month and e.day >= tomorrow_day):
                    print('you can use leitner now')
                    check(basic_csv,'30',id_0,questionToday_list)
                    check(basic_csv,'15',id_0,questionToday_list)
                    check(basic_csv,'7',id_0,questionToday_list)
                    check(basic_csv,'3',id_0,questionToday_list)
                    check(basic_csv,'1',id_0,questionToday_list)
                    check(basic_csv,'0',id_0,questionToday_list)
                    check(basic_csv,'another',id_0,list_another)
                    
                    sure = leitner(questionToday_list)
                    if sure != 'y' or sure != 'Y' or sure != '':
                        for row in list_another:
                            if (row[0] == '1' or row[0] == '3' or row[0] == '7' or row[0] == '15' or row[0] == '30') and row[4] == 'off':
                                edit_csv(basic_csv,row[0],row[1],row[2],row[3],'on')
                                
                            elif row[0] != '0' or row[0] != '1' or row[0] != '3' or row[0] != '7' or row[0] != '15' or row[0] != '30':
                            # TODO elif or else
                                edit_csv(basic_csv,row[0],row[1],row[2],str(int(row[3]) +1),row[4]) # TODO (row[4] or 'off')
                    tomorrow = datetime.date.today() + datetime.timedelta(days=1) # TODO
                    edit_time_csv(time_csv,tomorrow.year,tomorrow.month,tomorrow.day)
                    
                    if len(questionToday_list) == 0:
                        print('len list is zero (0). ')
                    # questionToday_list.sort() # TODO
                    # print(questionToday_list)
                    
                    for row in questionToday_list:
                        edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
                else:
                    questionToday_list = []
                    check_again(basic_csv,'30',questionToday_list)
                    check_again(basic_csv,'15',questionToday_list)
                    check_again(basic_csv,'7',questionToday_list)
                    check_again(basic_csv,'3',questionToday_list)
                    check_again(basic_csv,'1',questionToday_list)
                    check_again(basic_csv,'0',questionToday_list)
                    if len(questionToday_list) == 0:
                        print("you can'n use leitner now")
                        temp = input('but you can insert new word\n you want continue? (y/n): ')
                        if temp == 'y' or temp == 'Y' or temp == '':
                            check(basic_csv,'0',id_0,questionToday_list)
                            sure = leitner(questionToday_list) # TODO (sure = or not)
                            for row in questionToday_list:
                                edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
                    else:
                        print("you can just continue leitner now")
                        sure = leitner(questionToday_list) # TODO (sure = or not)
                        for row in questionToday_list:
                            edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
                        # print(questionToday_list)
                        if len(questionToday_list) == 0:
                            print('len list is zero (0). ')