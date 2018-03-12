#!/bin/sh

ROOT=./data
GEOROOT=./geo
ESTROOT=./newkey
LFILE=ACS_5yr_Seq_Table_Number_Lookup.txt
TBLIST=ACS_5yr_Tbl_List_B25.txt
STPOS=ACS_5yr_Tbl_Start_B25.txt
ESTPOS=ACS_5yr_Est_Pos_B25.txt
ESTLIST=ACS_5yr_Est_List_B25.txt
SEQLIST=ACS_5yr_Seq_List_B25.txt
TRLIST=ACS_5yr_Tracts.txt
BGLIST=ACS_5yr_Block_Groups.txt
EXTEST=ACS_5yr_Est_Extract_B25.txt
EXTESTTR=ACS_5yr_Tract_Est_Extract_B25.txt
EXTESTBG=ACS_5yr_Block_Group_Est_Extract_B25.txt

### Create list of keyed estimates and sequence files

echo "DEBUG: Extract Seq Number Lookup for B25 Tables"
grep 'B25' $ROOT/$LFILE | sort -u > $ROOT/$TBLIST

echo "DEBUG: Extract Table Start Number within Seq for B25 Tables"
grep -ivE ':|Median|Aggregate|Average|Mean|Gini|Quintile|Quartile|Population' $ROOT/$TBLIST \
	| grep -Ei 'Household|Occupied' \
	| awk -F, '$4 == " " && $5 > 0 {print $3","$3$2","$5}' > $ROOT/$STPOS

echo "DEBUG: Extract Detail Lines that are not Medians or Aggregates for B25 Tables"
grep 'B25' $ROOT/$LFILE \
	| grep -ivE ':|Median|Aggregate|Average|Mean|Gini|Quintile|Quartile' \
	| awk -F, '$4 > 0 && int($4) == $4 {print $3","$3$2","$4}' > $ROOT/tmplist

join -t, -j2 -a 1 -e "-1" -o 1.1,1.2,1.3,2.3 $ROOT/tmplist $ROOT/$STPOS > $ROOT/tmplist2
cat $ROOT/tmplist2 | awk -F, 'BEGIN{OFS=","} $4 != -1 {print $1,$2,$3;}' > $ROOT/$ESTLIST

echo "DEBUG: Create Field Positions for all Detailed Estimates"
join -t, -j 2 -o 2.1,2.2,1.3,2.3 $ROOT/$STPOS $ROOT/$ESTLIST > $ROOT/tmpfile
cat $ROOT/tmpfile | awk -F, '{print $1","($3+$4-1)}' > $ROOT/$ESTPOS

echo "DEBUG: Create Unique Seq List that Contain B25 Tables"
cat $ROOT/$ESTLIST | awk -F, '{print $1}' | sort -un > $ROOT/$SEQLIST

### Get geography file
#./create-us-geo.sh

### Unzip estimate files and concatenate

echo "DEBUG: Extract Files and Concatenate"
rm -f $ROOT/e20145.txt
find $ESTROOT -name 'e20145_01*.txt' -exec cat {} >> $ROOT/e20145.txt \;

### Extract selected keyed estimates

### Extract key to geo listing

echo "DEBUG: Extract GEO Lookup Numbers for Tracts and Block Groups"
grep ',140,00' $ROOT/g20145.csv | sed -r 's/,+/,/g' | awk -F, '{print $5","$6$7$8}'   	> $ROOT/${TRLIST}-debug
grep ',140,00' $ROOT/g20145.csv | sed -r 's/,+/,/g' | awk -F, '{print $5}' 				> $ROOT/$TRLIST
grep ',150,00' $ROOT/g20145.csv | sed -r 's/,+/,/g' | awk -F, '{print $5","$6$7$8$9}' 	> $ROOT/${BGLIST}-debug
grep ',150,00' $ROOT/g20145.csv | sed -r 's/,+/,/g' | awk -F, '{print $5}' 				> $ROOT/$BGLIST

cat $ESTROOT/e20145_0001000.txt | awk -F, 'BEGIN{OFS=",";} $8 == "" || ($8 < 10 && $8 > 2) {print $6,$7,$8;}' > $ROOT/tmpsmall
join -t, -j 1 $ROOT/$TRLIST $ROOT/tmpsmall > $ROOT/trlist-small.txt
join -t, -j 1 $ROOT/$BGLIST $ROOT/tmpsmall > $ROOT/bglist-small.txt
cat $ROOT/trlist-small.txt $ROOT/bglist-small.txt | sort | awk -F, '{print $1}' > $ROOT/trbglist-small.txt

### Extract geos from big file

#rm -f $ROOT/$EXTEST
#while read -r seq; do
	#AWKCODE=`cat $ROOT/$ESTPOS \
		#| awk -F, -v fseq=$seq 'BEGIN{ORS=",";} $1 == fseq {print "$"$2}' \
		#| sed 's/\,$//'`
	#grep ",${seq}," e20145.txt \
		#| awk -F, 'BEGIN{OFS=",";}{print $6,'$AWKCODE'; }' >> $ROOT/$EXTEST
#done < $ROOT/$SEQLIST

