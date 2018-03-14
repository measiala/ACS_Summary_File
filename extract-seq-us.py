#!/usr/bin/python3
##!/usr/local/bin/python3

import csv

ROOT='./data/'
INROOT='./webarchive/'
ESTROOT='./newkey/'

SEQFILE='ACS_5yr_Seq_Table_Number_Lookup.txt'

NotSimple = (':','Median','Aggregate','Average','Mean','Gini','Quintile','Quartile','Population')
UNotSimple = []
for s in NotSimple:
    UNotSimple.append(s.upper())

HHldOcc = ('Household','Occupied')
UHHldOcc = []
for s in HHldOcc:
    UHHldOcc.append(s.upper())

with open(INROOT + SEQFILE,"r",encoding='ISO-8859-1') as infile:
    incsv = csv.DictReader(infile)
    B25rows = []
    B25Tbls = []
    SimpleTbl = []

    for row in incsv:
        if row['Table ID'][0:3] == "B25":
            B25rows.append(row)
            if not row['Start Position'] == "":
                B25Tbls.append(row)
    #print(B25Tbls)
    print(len(B25Tbls))
    
    for row in B25Tbls:
        if not any(s in row['Table Title'] for s in UNotSimple):
            if any(s in row['Table Title'] for s in UHHldOcc):
                SimpleTbl.append(row)
                print(row['Line Number'],",",row['Start Position'])
                if row['Line Number'] == '' and not row['Start Position'] == "":
                    print(row['Sequence Number'],row['Sequence Number']+row['Table ID'],row['Start Position'])
    #print(SimpleTbl)
    print(len(SimpleTbl))

        
