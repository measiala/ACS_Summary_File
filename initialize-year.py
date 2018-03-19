#!/usr/bin/python3

import os
import errno
import sys
import urllib.request

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
urllib.request.urlretrieve(BASEURL + INTBLFILE,ARCHPATH + TBLFILE)

urllib.request.urlcleanup()
