#!/usr/bin/python3

import os.path
import sys
import time

import csv
import urllib.request
import zipfile
from multiprocessing.dummy import Pool

from fipsname import acssf_postal_to_name
from gen_funcs import is_number, is_integer, param_def, process_args

THREADS=1

param_list = process_args(sys.argv,['YYYY','PER','TBLID','SUMLVL'],['ST','CMP'])
for param in param_list:
    globals()[param[0]] = param[1]
CMP = '00'

YYP = YYYY + "/" + PER + "/"
DATAPATH='./data/'       + YYP
GEOPATH='./geo/'         + YYP
ARCHPATH='./webarchive/' + YYP
INPUTPATH='./input/'     + YYP

SEQFILE='ACS_' + YYYY + '_' + PER + '_Year_Seq_Table_Number_Lookup.txt'
GEOFILE='g' + YYYY + PER + '.csv'

start_time = time.time()

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
        if row['Table ID'].startswith(TBLID):
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

st_seq_list = []
for st in stlist:
    for seq in seqlist:
        st_seq_list.append([st,seq])

prep_time = time.time()
        
def get_data(st_seq):
    #print(st_seq)
    st = st_seq[0]
    seq = st_seq[1]
    stname = acssf_postal_to_name(st)
    st = st.lower()


    # Webname is same for all zip files
    BASEFILE = YYYY + PER + st + seq

    if PER == '1':
        SEQURL = BASEURL + stname + "/"
        code = '000'
    elif PER == '5':
        if st == 'dc':
            stname = stname.replace("of","Of")
        if SUMLVL in ['140','150']:
            SEQURL = BASEURL + stname + "/Tracts_Block_Groups_Only/"
            code = '140'
        else:
            SEQURL = BASEURL + stname + "/All_Geographies_Not_Tracts_Block_Groups/"
            code = '000'

    INFILENAME  = BASEFILE + '000' + '.zip'
    OUTFILENAME = BASEFILE + code  + '.zip'
    
    print('URI: ',SEQURL + FILENAME)

    if not os.path.isfile(ARCHPATH + OUTFILENAME):
        try:
            urllib.request.urlretrieve(SEQURL + INFILENAME,ARCHPATH + OUTFILENAME)
            print(FILENAME + " Downloaded")
        except urllib.error.HTTPError as e:
            print(e)
    else:
        print(OUTFILENAME + " File exists -- skipping")

    if zipfile.is_zipfile(ARCHPATH + INFILENAME):
        print("Extracting ", INFILENAME)
        archive = zipfile.ZipFile(ARCHPATH + INFILENAME,"r")
        for file in archive.namelist():
            if not os.path.isfile(INPUTPATH + file):
                archive.extract(file,path=INPUTPATH)
        archive.close()

result= Pool(THREADS).map(get_data,st_seq_list) # download 4 files at a time
      
end_time = time.time()

print("Prep time %s seconds" % (prep_time - start_time))
print("Download and extract time %s seconds" % (end_time - prep_time))
