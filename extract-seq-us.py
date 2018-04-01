#!/usr/bin/python3

import os.path
import sys
import time

import csv
import urllib.request
import zipfile
#from multiprocessing.dummy import Pool
import concurrent.futures

import config
from fipsname import acssf_postal_to_name
from gen_funcs import is_number, is_integer, param_def, process_args

def init():
    param_list = process_args(sys.argv,['YYYY','PER','TBLID','SUMLVL'],['ST','CMP'])
    for param in param_list:
        globals()[param[0]] = param[1]

    global YYP,DATAPATH,GEOPATH,ARCHPATH,INPUTPATH,SEQFILE,GEOFILE,BASEURL
    
    YYP = YYYY + "/" + PER + "/"
    DATAPATH='./data/'       + YYP
    GEOPATH='./geo/'         + YYP
    ARCHPATH='./webarchive/' + YYP
    INPUTPATH='./input/'     + YYP

    SEQFILE='ACS_' + YYYY + '_' + PER + '_Year_Seq_Table_Number_Lookup.txt'
    GEOFILE='g' + YYYY + PER + '.csv'

    BASEURL = 'https://www2.census.gov/programs-surveys/acs/summary_file/' \
              + YYYY + '/data/' + PER + '_year_seq_by_state/'

###
### Extract SEQ file needs
###

def get_seqlist():
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

    return seqlist
    #print("Number of detailed estimates = ",len(tblname))
    #print("Sorted list of sequence files = ",seqlist)

###
### Extract Geographies
###

def get_stlist():
    with open(DATAPATH + GEOFILE,"r",encoding='ISO-8859-1') as infile:
        incsv = csv.DictReader(infile)
        geolist = []
        stset = set()
        for row in incsv:
            if row['SUMLEVEL'] == SUMLVL and row['COMPONENT'] == CMP:
                geolist.append((row['MATCHID'],row['STUSAB'],row['LOGRECNO'],
                                row['GEOID'],row['NAME']))
                stset.add(row['STUSAB'])
    stlist = list(stset)
    stlist.sort()
    return stlist

###
### Download data files for States in stlist and Sequences in seqlist
###

def generate_st_seq(stlist,seqlist):
    st_seq_list = []
    for st in stlist:
        for seq in seqlist:
            st_seq_list.append([st,seq])
    return st_seq_list

#prep_time = time.time()
        
def get_data(st_seq):
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

    INZIPNAME  = BASEFILE + '000' + '.zip'
    OUTZIPNAME = BASEFILE + code  + '.zip'

    if not os.path.isfile(ARCHPATH + OUTZIPNAME):
        print("Downloading %s as %s" % (INZIPNAME,OUTZIPNAME))
        try:
            urllib.request.urlretrieve(SEQURL + INZIPNAME,ARCHPATH + OUTZIPNAME)
        except urllib.error.HTTPError as e:
            return e
    else:
        print(OUTZIPNAME + " File exists -- skipping")

    if zipfile.is_zipfile(ARCHPATH + OUTZIPNAME):
        with zipfile.ZipFile(ARCHPATH + OUTZIPNAME,"r") as archive:
            for file in archive.namelist():
                outfilename = file.replace('000.txt',code + '.txt')
                if not os.path.isfile(INPUTPATH + outfilename):
                    with open(INPUTPATH + outfilename,'w') as outfile:
                        outcsv = csv.writer(outfile)
                        with archive.open(file,mode='r') as infile:
                            for line in infile:
                                row = line.decode('ascii').rstrip().split(',')
                                row[0] = row[2].lower() + row[5]
                                del(row[1:6])
                                outcsv.writerow(row)
                    return 'Extracted'
                else:
                    return 'Skipped'
    else:
        return 'Bad ZIP'

def main(stseq_list):
    with concurrent.futures.ProcessPoolExecutor(max_workers=config.PROCS) as executor:
        for st_seq, result in zip(stseq_list,executor.map(get_data,stseq_list)):
            print( st_seq[0] + st_seq[1] + ' is ' + result )

if __name__ == '__main__':
    start_time = time.time()

    init()
    stlist = get_stlist()
    #stlist = ['AL']
    seqlist = get_seqlist()
    st_seq_list = generate_st_seq(stlist,seqlist)
    
    main(st_seq_list)

    end_time = time.time()
    
    print("Download and extract time %s seconds" % (end_time - start_time))
    

