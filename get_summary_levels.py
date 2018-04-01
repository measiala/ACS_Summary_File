#!/usr/bin/python3

import os.path
import sys

import xlrd
import urllib.request
import csv
from gen_funcs import param_def, process_args

param_list = process_args(sys.argv,['YYYY'])
for param in param_list:
    globals()[param[0]] = param[1]

BASEURL='https://www2.census.gov/programs-surveys/acs/summary_file/' + YYYY + '/documentation/tech_docs/'
FILENAME='ACS_' + YYYY + '_SF_5YR_Appendices.xls'

FULLURL = BASEURL + FILENAME
ARCHPATH  = './webarchive/' + YYYY + '/'
INPUTPATH = './input/' + YYYY + '/'

if not os.path.isfile(ARCHPATH + FILENAME):
    try:
        urllib.request.urlretrieve(BASEURL + FILENAME,ARCHPATH + FILENAME)
    except urllib.error.HTTPError as e:
        print(e)

# Assumptions on workbook
# 1) Appendix A provides table availability by summary level and relevant sequence file
# 2) Appendix B provides summary level availability by product
# 3) Appendix B layout: SUMLVL, CMP, NAME, FLAG_AVAIL_1, FLAG_AVAIL_5, DIRECTORY

wb = xlrd.open_workbook(ARCHPATH + FILENAME)
ws = wb.sheet_by_name('Appendix B')

sumlvl_dict  = {}
sumlvl_dict1 = {}
sumlvl_dict5 = {}
for row in range(1,ws.nrows):
    SUMLVL = str(ws.cell_value(row,0))
    if len(SUMLVL) > 3:
        SUMLVL = SUMLVL[0:3]
    CMP    = str(ws.cell_value(row,1))
    if len(CMP) > 2:
        CMP = CMP[0:2]
    NAME   = str(ws.cell_value(row,2))
    FLAG_AVAIL_1 = ws.cell_value(row,3).lower()
    FLAG_AVAIL_5 = ws.cell_value(row,4).lower()

    # General summary level dictionary with no flag applied
    sumlvl_dict[(SUMLVL, CMP)] = NAME

    # Summary level dictionary with 1-year available flag applied
    if FLAG_AVAIL_1 == 'x':
        sumlvl_dict1[(SUMLVL, CMP)] = NAME

    # Summary level dictionary with 5-year available flag applied
    if FLAG_AVAIL_5 == 'x':
        sumlvl_dict5[(SUMLVL, CMP)] = NAME
        
#print(sumlvl_dict1)
#try:
#    print(sumlvl_dict1['140','00'])
#except KeyError as error:
#    print("Summary level not available for 1-year estimates.")

DICTFILE = 'sumlvl_dict.csv'

with open(INPUTPATH + DICTFILE,'w') as outfile:
    outcsv = csv.writer(outfile)
    for key, val in sumlvl_dict.items():
        outcsv.writerow([key, val])
with open(INPUTPATH + '1/' + DICTFILE,'w') as outfile:
    outcsv = csv.writer(outfile)
    for key, val in sumlvl_dict1.items():
        outcsv.writerow([key, val])
with open(INPUTPATH + '5/' + DICTFILE,'w') as outfile:
    outcsv = csv.writer(outfile)
    for key, val in sumlvl_dict5.items():
        outcsv.writerow([key, val])
