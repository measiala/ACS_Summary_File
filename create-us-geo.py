##!/usr/local/bin/python3
#!/usr/bin/python3

YYYY="2016"
PER="1"

GEOPATH="./geo/"
DATAPATH="./data/"

import csv
import os
import fnmatch

files = os.listdir(GEOPATH)
csvfiles = sorted(fnmatch.filter(files,"g" + YYYY + PER + '??.csv'))

with open(DATAPATH + "g" + YYYY + PER + ".csv","w") as outcsv:
    outfile = csv.writer(outcsv,quoting=csv.QUOTE_MINIMAL)
    for csvfile in csvfiles:
        with open(GEOPATH + csvfile,"r",encoding='ISO-8859-1') as incsv:
            infile = csv.reader(incsv,quotechar='"')
            for row in infile:
                row[1] = row[1].lower() + row[4]
                del row[0]
                del row[3]
                outfile.writerow(row)

