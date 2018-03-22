#!/usr/bin/python3

from multiprocessing.dummy import Pool
import urllib.request
from fipsname import acssf_fips_to_name,acssf_name_to_postal

YYYY='2016'
PER='5'

BASEURL = 'https://www2.census.gov/programs-surveys/acs/summary_file/' \
          + YYYY + '/data/' + PER + '_year_seq_by_state/'
ROOTFILE='g' + YYYY + PER

GEOPATH='./test/'

fips_list = ['00']
for nst in range(1,57):
    if not nst in [3,7,14,43,52]:
        st = str(nst).zfill(2)
        fips_list.append(st)
fips_list.append('72')

def download_geo(st):
    stname = acssf_fips_to_name(st)
    pstcode = acssf_name_to_postal(stname).lower()

    if PER == '1':
        URLPATH = BASEURL + stname + "/"
    elif PER == '5':
        if st == '11':
            stname = stname.replace("of","Of")
        URLPATH = BASEURL + stname + "/Tracts_Block_Groups_Only/"

    FILENAME =  ROOTFILE + pstcode + '.csv'
    STURL = URLPATH + FILENAME

    #print(STURL)

    try:
        urllib.request.urlretrieve(STURL,GEOPATH + FILENAME)
    except urllib.error.HTTPError as e:
        print(FILENAME + ': ' + e)
   

result= Pool(4).map(download_geo, fips_list) # download 4 files at a time

