#!/bin/ksh

ESTROOT=./newkey
SRCROOT=./tab4/sumfile/prod/2010thru2014/group2

find $SRCROOT -name "e20145ca[0-9]*000.txt" -printf "%f\n" \
	| awk '{print substr($0,9,4);}' \
	| sort -u > $ESTROOT/seq-list.txt

while read SEQ; do
	rm -f $ESTROOT/e20145_${SEQ}000.txt
	echo $SEQ
	find $SRCROOT -name "e20145[a-z][a-z]${SEQ}000.txt" -print \
		| sort \
		| xargs -I'{}' cat {} \
		| ./create-us-seq.awk > $ESTROOT/e20145_${SEQ}000.txt
done < $ESTROOT/seq-list.txt
