import csv
from datetime import date


def convert_to_json():
    csv_file = csv.DictReader(open('temp.csv', 'r'))
    json_list = []
    for row in csv_file:
        json_list.append(row)
    return json_list

def append_in_list(list,dest):
    with open(dest, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list)


def get_date():
    today = date.today()
    return today.strftime("%m/%d/%y")