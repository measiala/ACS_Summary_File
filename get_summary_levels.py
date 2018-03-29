#!/usr/bin/python3

import os.path
import sys

import xlrd
import urllib.request
from gen_funcs import param_def, process_args

YYYY='2016'

BASEURL='https://www2.census.gov/programs-surveys/acs/summary_file/' + YYYY + '/documentation/tech_docs/'
FILENAME='ACS_' + YYYY + '_SF_5YR_Appendices.xls'

FULLURL = BASEURL + FILENAME
ARCHPATH = './webarchive/' + YYYY + '/'

if not os.path.isfile(ARCHPATH + FILENAME):
    try:
        urllib.request.urlretrieve(BASEURL + FILENAME,ARCHPATH + FILENAME)
    except urllib.error.HTTPError as e:
        print(e)

wb = xlrd.open_workbook(ARCHPATH + FILENAME)
ws = wb.sheet_by_name('Appendix B')

dict = []
dict.append([ 'SUMLVL', 'CMP', 'NAME' ])
for row in range(1,ws.nrows):
    dict.append([ws.cell(row,0)[1],ws.cell(row,1)[1],ws.cell(row,2)[1]])

print(dict)
print("Number of rows is ", ws.nrows)
print("Number of columns is ",ws.ncols)
