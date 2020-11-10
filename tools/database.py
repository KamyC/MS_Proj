import csv
import os.path
import tools.util

def write_in(str , label):
    with open("tempDatabase/temp.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = [str,label]
        writer.writerow(row)

def write_user_to_temp_database(user_info_list):
    with open("tempDatabase/users.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_info_list)

def find_user_in_temp_database(emailInput, pswInput):
    with open("tempDatabase/users.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        userInfo = []
        for line in reader:
            if (emailInput == line[1]) and (pswInput == line[2]):
                userInfo = line
                return userInfo
        return userInfo

def write_new_in_list(list,dest):
    tag_list = ["Twitter Content","Label","Date","Confidence Score"]
    with open(dest, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(tag_list)
        wr.writerow(list)

def write_for_user(user,content, label, date, score):
    file_name = "tempDatabase/"+user+".csv"
    list = [content,label,date,score];
    if os.path.exists(file_name):
        tools.util.append_in_list(list,file_name)
    else:
        write_new_in_list(list, file_name)
