#!/usr/bin/python3
##!/usr/local/bin/python3

import sys
import csv
from fipsname import *

import urllib.request
import zipfile

def is_number(s):
    try:
        complex(s)
    except ValueError:
        return False
    return True

def is_integer(s):
    try:
        int(s)
    except ValueError:
        return False
    return True

print(sys.argv,len(sys.argv))

if len(sys.argv) < 5 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage: " + sys.argv[0] + " [ -h | --help ]")
    print("       " + sys.argv[0] + " YYYY Period [ TableID | TableStart] SUMLVL")
    print("Where:")
    print("       YYYY is between 2010 and 2019")
    print("       PER is either 1 or 5 depending on the period of data used.")
    print("       TableID is up to length 6 consisting of a letter B/C/K followed by up to 5 digits.")
    print("       SUMLVL is the 3-digit summary level including leading zeros.")
#    print("       CMP is the 2-digit component for the summary level if available.")
#    print("       ST is the optional 2-digit FIPS code for the state of interest.")
    exit(3)
elif len(sys.argv) == 5:
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
    if sys.argv[3][0] not in ['B','C','K']:
        print("Table ID must begin with B, C, or K.")
    elif sys.argv[3][1:].isnumeric():
        if len(sys.argv[3]) < 7:
            tblsubstr = sys.argv[3]
        else:
            print("Check your input match string.")
            exit(2)
    else:
        print("Match string must start with B, C, or K and be followed by 1-5 digits.")
        exit(2)
    if not (len(sys.argv[4]) == 3 and sys.argv[4].isnumeric()):
        print("Summary level should be a 3 digit number including any leading zeros.")
        exit(2)
    else:
        SUMLVL = sys.argv[4]
        CMP = '00'  # Simplify searches for now and set Components = '00'
        if not SUMLVL in ['010','020','030','250']:
            ST = '26'
            
elif len(sys.argv) > 5:
    print("Too many arguments. See " + sys.argv[0] + " -h for help.")
    exit(2)
else:
    print("Confusion abound.")

YYP = YYYY + "/" + PER + "/"
DATAPATH='./data/'       + YYP
GEOPATH='./geo/'         + YYP
ARCHPATH='./webarchive/' + YYP
INPUTPATH='./input/'     + YYP

SEQFILE='ACS_' + YYYY + '_' + PER + '_Year_Seq_Table_Number_Lookup.txt'
GEOFILE='g' + YYYY + PER + '.csv'

# Input Table (e.g., B25001) or Series (e.g., B25)

###
### Extract SEQ file needs
###

with open(ARCHPATH + SEQFILE,"r",encoding='ISO-8859-1') as infile:
    incsv = csv.DictReader(infile)

    tblrows = []
    tblname = [[ 'TABLEID','SEQNO','STARTPOS','TOTCELLS','TOTSEQCELLS','TITLE' ]]
    tbldet  = [[ 'TABLEID','SEQNO','POSITION','LINENO','STUB' ]]
    seqset = set()
    
    for row in incsv:
        if row['Table ID'].startswith(tblsubstr):
            tblrows.append(row)
            if is_integer(row['Start Position']):
                start_position = int(row['Start Position'])
                tblname.append([row['Table ID'],row['Sequence Number'],
                                start_position, row['Total Cells in Table'],
                                row['Total Cells in Sequence'],row['Table Title']])
            elif is_integer(row['Line Number']):
                line_number = int(row['Line Number'])
                position = start_position + line_number - 1
                tbldet.append([row['Table ID'],row['Sequence Number'],
                               position,line_number,row['Table Title']])
                seqset.add(row['Sequence Number'])

    seqlist = list(seqset)
    seqlist.sort()
    
    print("Number of detailed estimates = ",len(tblname))
    print("Sorted list of sequence files = ",seqlist)

###
### Extract Geographies
###

with open(DATAPATH + GEOFILE,"r",encoding='ISO-8859-1') as infile:
    incsv = csv.DictReader(infile)

    geolist = []
    stset = set()
    
    for row in incsv:
        if row['SUMLEVEL'] == SUMLVL and row['COMPONENT'] == CMP:
            geolist.append((row['MATCHID'],row['STUSAB'],row['LOGRECNO'],row['GEOID'],row['NAME']))
            stset.add(row['STUSAB'])

    print("Number of geographies = ",len(geolist))

stlist = list(stset)
stlist.sort()

print("Need to download files from ",stlist)

###
### Download data files for States in stlist and Sequences in seqlist
###

BASEURL = 'https://www2.census.gov/programs-surveys/acs/summary_file/' \
          + YYYY + '/data/' + PER + '_year_seq_by_state/'

for st in stlist:
    stname = acssf_postal_to_name(st)
    st = st.lower()
    
    if PER == '1':
        SEQURL = BASEURL + stname + "/"
    elif PER == '5':
        if SUMLVL in ['140','150']:
            SEQURL = BASEURL + stname + "/Tracts_Block_Groups_Only/"
        else:
            SEQURL = BASEURL + stname + "/All_Geographies_Not_Tracts_Block_Groups/"

    for seq in seqlist:
        FILENAME = YYYY + PER + st + seq + '000.zip'
        print('URI: ',SEQURL + FILENAME)
        # We should test for existence of file to avoid unnecessary downloads here need SUMLVL check tho
        urllib.request.urlretrieve(SEQURL + FILENAME,ARCHPATH + FILENAME)

        if zipfile.is_zipfile(ARCHPATH + FILENAME):
            print("Extracting ",FILENAME)
            archive = zipfile.ZipFile(ARCHPATH + FILENAME,"r")
            for file in archive.namelist():
                archive.extract(file,path=INPUTPATH)
            archive.close()
            
urllib.request.urlcleanup()

#########################

#for st in stlist:
#    for row
#    st = st.lower()
