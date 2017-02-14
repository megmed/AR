import csv
import logging
from datetime import datetime

logging.basicConfig(filename='extract.log', level=logging.INFO)


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return abs((d2 - d1).seconds)


with open('actions_1_von_4.csv', 'r', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    sortedlist = sorted(dataReader, key=lambda row: (row[0], row[1]), reverse=True)
    i = 0
    previousRow = None
    previousUserId = None
    for row in sortedlist:
        print(', '.join(row))


        if i > 1:
            print(days_between(row[1], previousRow[1]))
            if row[0] != previousUserId:
                print(row[0])
        else:
            print(row)
        if i > 30:
            break
        previousUserId = row[0]
        previousRow = row
        i += 1
