#!/usr/bin/python3

import sys
import os
import fnmatch
import csv

from fipsname import acssf_postal_to_name
from gen_funcs import is_number, is_integer, param_def, process_args

param_list = process_args(sys.argv,['YYYY','PER']) #,'TBLID','SUMLVL'],['ST','CMP'])
for param in param_list:
    globals()[param[0]] = param[1]

YYP = YYYY + "/" + PER + "/"
INPUTPATH='./input/' + YYP
DATAPATH='./data/' + YYP

BASE_EST='e' + YYYY + PER

files = os.listdir(INPUTPATH)
estfiles = sorted(fnmatch.filter(files,BASE_EST + '??????000.txt'))

seq_set = set()
for file in estfiles:
    seq = file[8:12]
    if seq.isdigit():
        seq_set.add(seq)

seq_list = sorted(seq_set)

for seq in seq_list:
    with open(DATAPATH + BASE_EST + '_' + seq + '.csv',"w") as outfile:
        outcsv = csv.writer(outfile)
        est_seq = sorted(fnmatch.filter(estfiles,BASE_EST + '??' + seq + '000.txt'))
        for file in est_seq:
            with open(INPUTPATH + file,"r") as infile:
                incsv = csv.reader(infile)
                for row in incsv:
                    row[0] = row[2].lower() + row[5]
                    del(row[1:6])
                    outcsv.writerow(row)
                
