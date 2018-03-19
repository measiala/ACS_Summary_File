#!/usr/bin/python3

import csv
import sys

import os

import fnmatch
import urllib.request
from fipsname import *

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
    
GEOPATHYY = "./geo/"  + YYYY + "/"
GEOPATH   = GEOPATHYY + PER + "/"
DATAPATH="./data/" + YYYY + "/" + PER + "/"

BASEURL = 'https://www2.census.gov/programs-surveys/acs/summary_file/' \
          + YYYY + '/data/' + PER + '_year_seq_by_state/'
ROOTFILE='g' + YYYY + PER

def down_load_geo(nst):
    st = str(nst).zfill(2)
    stname = acssf_fips_to_name(st)
    pstcode = acssf_name_to_postal(stname).lower()

    if PER == '1':
        URLPATH = BASEURL + stname + "/"
    elif PER == '5':
        if nst == 11:
            stname = stname.replace("of","Of")
        URLPATH = BASEURL + stname + "/Tracts_Block_Groups_Only/"

    FILENAME =  ROOTFILE + pstcode + '.csv'
    STURL = URLPATH + FILENAME

    print(STURL)

    urllib.request.urlretrieve(STURL,GEOPATH + FILENAME)

## Download state-level csv files into geo directory
print("Downloads beginning.")
for nst in range(1,57):
    if not nst in [3,7,14,43,52]:
        down_load_geo(nst)
down_load_geo(72)
urllib.request.urlcleanup()
print("Downloads complete.")

## Concatenate to make US-level csv files into data directory

files = os.listdir(GEOPATH)
csvfiles = sorted(fnmatch.filter(files,ROOTFILE + '??.csv'))

print("Create US-level file.")
with open(DATAPATH + ROOTFILE + ".csv","w") as outfile:
    outcsv = csv.writer(outfile,quoting=csv.QUOTE_MINIMAL)
    with open(GEOPATHYY + 'g' + YYYY + '.lay',"r") as layfile:
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
print("US-level file complete.")
