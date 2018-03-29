#!/usr/bin/python3

import sys
import os
import csv
import fnmatch
import urllib.request
from gen_funcs import is_number, is_integer, param_def, process_args
from fipsname import acssf_name_to_postal, acssf_fips_to_name

#print(sys.argv)
param_list = process_args(sys.argv,['YYYY','PER'])
for param in param_list:
    globals()[param[0]] = param[1]
    
GEOPATHYY = "./geo/"  + YYYY + "/"
GEOPATH   = GEOPATHYY + PER + "/"
DATAPATH="./data/" + YYYY + "/" + PER + "/"

BASEURL = 'https://www2.census.gov/programs-surveys/acs/summary_file/' \
          + YYYY + '/data/' + PER + '_year_seq_by_state/'
ROOTFILE='g' + YYYY + PER

GEOLAYDIR = './geo/'
GEOLAY= 'gyyyyp'

# old definition
# GEOLAYDIR = GEOPATHYY
# GEOLAY= 'g' + YYYY + PER

def down_load_geo(nst):
    st = str(nst).zfill(2)
    stname = acssf_fips_to_name(st)
    pstcode = acssf_name_to_postal(stname).lower()

    if PER == '1':
        URLPATH = BASEURL + stname + "/"
    elif PER == '5':
        if nst == 11:
            stname = stname.replace("of","Of")
        URLPATH = BASEURL + stname + "/Tracts_Block_Groups_Only/"

    FILENAME =  ROOTFILE + pstcode + '.csv'
    STURL = URLPATH + FILENAME

    print(STURL)

    if not os.path.isfile(GEOPATH + FILENAME):
        try:
            urllib.request.urlretrieve(STURL,GEOPATH + FILENAME)
            print("Downloaded ",FILENAME)
        except urllib.error.HTTPError as e:
            print(FILENAME + ': ' + e)
    else:
        print("Skipping ",FILENAME)

## Download state-level csv files into geo directory

print("Downloads beginning.")
down_load_geo(00)
for nst in range(1,57):
    if not nst in [3,7,14,43,52]:
        down_load_geo(nst)
down_load_geo(72)

print("Downloads complete.")

## Concatenate to make US-level csv files into data directory

files = os.listdir(GEOPATH)
csvfiles = sorted(fnmatch.filter(files,ROOTFILE + '??.csv'))

print("Create US-level file.")
with open(DATAPATH + ROOTFILE + ".csv","w") as outfile:
    outcsv = csv.writer(outfile,quoting=csv.QUOTE_MINIMAL)
    with open(GEOLAYDIR + GEOLAY + '.lay',"r") as layfile:
        laycsv = csv.reader(layfile)
        for row in laycsv:
            row[0] = 'MATCHID'
        outcsv.writerow(row)
    for csvfile in csvfiles:
        with open(GEOPATH + csvfile,"r",encoding='ISO-8859-1') as infile:
            incsv = csv.reader(infile,quotechar='"')
            for row in incsv:
                row[0] = row[1].lower() + row[4]
                outcsv.writerow(row)
print("US-level file complete.")
