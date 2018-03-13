#!/usr/local/bin/python3

import csv

ROOT='./data/'
INROOT='./input/'
ESTROOT='./newkey/'

SEQFILE='ACS_5yr_Seq_Table_Number_Lookup.txt'


with open(INROOT + SEQFILE,"r") as infile:
    incsv = csv.DictReader(infile)
    outcsv = []
    for row in incsv:
        if row['Table ID'][0:3] == "B025":
            outcsv.append(row)
    print(outcsv)
        
