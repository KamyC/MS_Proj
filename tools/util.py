import csv
from datetime import date
from itertools import islice

def append_in_list(list,dest):
    with open(dest, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list)


def get_date():
    today = date.today()
    return today.strftime("%m/%d/%y")


def find_user_information(usrname):
    if usrname:
        filename = "tempDatabase/"+usrname+".csv"
        each_count = get_each_count(filename)
        time_cnt = get_date_cnt(filename)
        past_ten_tweets = get_past_ten_tweets(usrname)
        data = {
            "name" : usrname,
            "spam_cnt": each_count[0],
            "benign_cnt": each_count[1],
            "time_cnt" : time_cnt,
            "past_ten_tweets":past_ten_tweets
        }
        return data
def get_total_number(username):
    if username:
        filename = "tempDatabase/" + username + ".csv"
        with open(filename, 'rb') as f:
            return len(f.readlines())

def get_each_count(filename):
    spam_cnt = 0
    benign_cnt = 0
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Label'] == "sus_spam":
                spam_cnt+=1
            else:
                benign_cnt+=1
    return (spam_cnt,benign_cnt)

def get_date_cnt(filename):
    dict={}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Date"] in dict:
                dict[row["Date"]] +=1
            else:
                dict[row["Date"]] = 0
    return dict

def get_past_ten_tweets(usrname):
    filename = "tempDatabase/"+usrname+".csv"
    tweet_list= []
    total = get_total_number(usrname)
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in islice(reader, total-10, total):  # last 10 only
            tweet_list.append(row['Twitter Content'])
    return tweet_list
