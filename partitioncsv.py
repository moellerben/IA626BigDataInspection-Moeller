# Takes a very large CSV and cuts out the first N rows

import csv

NUM_ROWS = 100000
SKIP_ROWS = 1000
IN_FN = "trip_data_4.csv"
OUT_HEAD_FN = "trip_data_4_head.csv"
OUT_SKIP_FN = "trip_data_4_skip.csv"

headdata = []
skiprowdata = []

with open(IN_FN, newline='') as incsv:
    inreader = csv.reader(incsv)
    n = 0
    for row in inreader:
        n += 1
        headdata.append(row)
        if n >= NUM_ROWS:
            break
    n = 0
    for row in inreader:
        if n % SKIP_ROWS == 0:
            skiprowdata.append(row)
        if n % 1000000 == 0:
            print(n)
        n += 1

#print(len(data))

with open(OUT_HEAD_FN, 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    for row in headdata:
        writer.writerow(row)

with open(OUT_SKIP_FN, 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    for row in skiprowdata:
        writer.writerow(row)
