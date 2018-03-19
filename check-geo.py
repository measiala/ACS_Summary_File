#!/usr/bin/python

import csv

numrec = set()

with open('./data/g20161.csv',"r") as infile:
	incsv = csv.reader(infile)
	for row in incsv:
		numrec.add(len(row))
   
print(numrec)
