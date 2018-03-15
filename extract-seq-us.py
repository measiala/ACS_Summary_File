#!/usr/bin/python3
##!/usr/local/bin/python3

import sys
import csv

if len(sys.argv) = 1:
    if sys.argv[1][0] not in ['B','C','K']:
        print("Table ID must begin with B, C, or K.")
    elif sys.argv[1][1:].isnum():
        if len(sys.argv[1]) < 7:
            tblsubstr = sys.argv[1]
        else:
            print("Check your input match string.")
elif len(sys.argv) > 1:
    print("Too many arguments. See " + sys.argv[0] + " -h for help.")
elif len(sys.argv) < 1 or sys.argv == "-h" or sys.argv = "--help":
    print("Usage: " + sys.argv[0] + " [ -h | --help ]")
    print("       " + sys.argv[0] + " [ TableID | TableStart]")
    exit(3)

ROOT='./data/'
INROOT='./webarchive/'

SEQFILE='ACS_5yr_Seq_Table_Number_Lookup.txt'

# Input Table (e.g., B25001) or Series (e.g., B25)

SERIES=B25
TABLE=
#TABLE=B25001

with open(INROOT + SEQFILE,"r",encoding='ISO-8859-1') as infile:
    incsv = csv.DictReader(infile)

    tblrows = []
    tblname = []
    tbldet  = []
    
    for row in incsv:
        if row['Table ID'][0:len(tblsubstr)] == tblsubstr:
            tblrows.append(row)
            if not row['Start Position'] == "":
                tblname.append(row)
            elif not row['Line Number'] == "":
                tbldet.append(row)
    print(len(tblname))
    

        
