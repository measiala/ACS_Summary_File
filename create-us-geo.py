#!/usr/bin/python3
##!/usr/local/bin/python3

import csv
import os
import sys
import fnmatch

if len(sys.argv) < 3 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage: " + sys.argv[0] + " [ -h | --help ]")
    print("       " + sys.argv[0] + " YYYY Period")
    exit(3)
elif len(sys.argv) == 3:
    if int(sys.argv[1]) in range(2010,2020):
        YYYY = sys.argv[1]
    else:
        print("Enter a year between 2010 and 2019.")
        exit(2)
    if int(sys.argv[2]) in [1,5]:
        PER = sys.argv[2]
    else:
        print("Period must be equal to either 1 or 5.")
        exit(2)
elif len(sys.argv) > 3:
    print("Too many arguments. See " + sys.argv[0] + " -h for help.")
    exit(2)
else:
    print("Confusion abound.")
    
GEOPATH ="./geo/"  + YYYY + "/"
DATAPATH="./data/" + YYYY + "/" + PER + "/"

files = os.listdir(GEOPATH + "/" + PER)
csvfiles = sorted(fnmatch.filter(files,"g" + YYYY + PER + '??.csv'))

with open(DATAPATH + "/g" + YYYY + PER + ".csv","w") as outfile:
    outcsv = csv.writer(outfile,quoting=csv.QUOTE_MINIMAL)
    with open(GEOPATH + 'g' + YYYY + '.lay',"r") as layfile:
        laycsv = csv.reader(layfile)
        for row in laycsv:
            row[0] = 'MATCHID'
            del row[4]
        outcsv.writerow(row)
    for csvfile in csvfiles:
        with open(GEOPATH + csvfile,"r",encoding='ISO-8859-1') as infile:
            incsv = csv.reader(infile,quotechar='"')
            for row in incsv:
                row[0] = row[1].lower() + row[4]
                del row[4]
                outcsv.writerow(row)

