#!/usr/bin/python3

import sys
import os
import fnmatch
import csv
from multiprocessing.dummy import Pool

from fipsname import acssf_postal_to_name
from gen_funcs import is_number, is_integer, param_def, process_args

### Number of multiprocessing threads
THREADS=2

### Read in arguments
param_list = process_args(sys.argv,['YYYY','PER'])
for param in param_list:
    globals()[param[0]] = param[1]

### Define pathnames
YYP = YYYY + "/" + PER + "/"
INPUTPATH='./input/' + YYP
DATAPATH='./data/' + YYP

### Define root filename for estimates files
BASE_EST='e' + YYYY + PER

### Create list of all estimates files (ignores MOE files)
files = os.listdir(INPUTPATH)
estfiles = sorted(fnmatch.filter(files,BASE_EST + '??????000.txt'))

### Create unduplicated sorted list of seq files
seq_set = set()
for file in estfiles:
    seq = file[8:12]
    if seq.isdigit():
        seq_set.add(seq)
seq_list = sorted(seq_set)

### Routine to create a rolled up file of all estimates by seq
def create_nat_seq(seq):
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

### Call the multithreaded routine
result= Pool(THREADS).map(create_nat_seq, seq_list)
                
