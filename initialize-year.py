#!/usr/bin/python3

import os
import errno
import sys
import urllib.request
from gen_funcs import is_number, is_integer, param_def, process_args

param_list = process_args(sys.argv,['YYYY','PER'])
for param in param_list:
    globals()[param[0]] = param[1]

YYP = YYYY + "/" + PER + "/"
GEOPATH   = './geo/'        + YYP
DATAPATH  = './data/'       + YYP
INPUTPATH = './input/'      + YYP
ARCHPATH  = './webarchive/' + YYP

def create_directory(mydir):
    if not os.path.exists(mydir):
        try:
            os.makedirs(mydir)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise

create_directory(GEOPATH)
create_directory(DATAPATH)
create_directory(INPUTPATH)
create_directory(ARCHPATH)

BASEURL = 'https://www2.census.gov/programs-surveys/acs/summary_file/' \
          + YYYY + '/documentation/user_tools/'
INTBLFILE = 'ACS_' + PER + 'yr_Seq_Table_Number_Lookup.txt'
TBLFILE = 'ACS_' + YYYY + '_' + PER + '_Year_Seq_Table_Number_Lookup.txt'

print("Retriving ",BASEURL + INTBLFILE)
try:
    urllib.request.urlretrieve(BASEURL + INTBLFILE,ARCHPATH + TBLFILE)
except urllib.error.HTTPError as e:
    print(e)

