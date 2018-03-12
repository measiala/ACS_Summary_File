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

rm -f $ROOT/$EXTEST
echo "DEBUG: Extract Estimates in SEQ GEO sort order."
while read -r seq; do
	echo "--Create AWK Extract code for ${seq}"
	AWKCODE=`cat $ROOT/$ESTPOS \
		| awk -F, -v fseq=$seq 'BEGIN{ORS=",";} $1 == fseq {print "$"$2}' \
		| sed 's/\,$//'`
	echo "--Create SEQ GEO Extract for ${seq}"
	#GEOLIST=`cat data/trbglist-small.txt | tr '\012' '\174' | sed -e 's/|$//g'`
	GEOLIST=`cat data/trbglist-small.txt | tr '\012' '\174' | sed -e 's/|$//g' | sed 's/|/|^/g' | sed 's/^/^/'`
	grep -E "$GEOLIST" $ESTROOT/e20145_${seq}000.txt \
		| awk -F, 'BEGIN{OFS=",";ORS="\n"} {print $5,$6,'$AWKCODE'; }' \
		| sed -r 's/\,\,+/\,/g' \
		| sed -e 's/\,$//g' \
		| awk -F, '{printf "%s,%s",$1,$2; for (i=3;i<NF+1;i++) if ($i != 0) printf ",%s",$i; 1; printf "\n";}' \
		| awk -F, 'NF>2' > $ROOT/tmpgeo
	while read -r line; do
		echo $line \
			| awk -F, 'BEGIN{OFS=","; ORS=""}{print $2,$1; print ",";}' >> $ROOT/$EXTEST
		echo $line \
			| awk -F, '{for (i=3;i<NF+1;i++) print $i;}' \
			| sort -un \
			| tr '\012' '\054'  \
			| awk -F, '{for (i=1;i<NF-1;i++) printf "%s,",$i; print $(NF-1);}' >> $ROOT/$EXTEST
	done < $ROOT/tmpgeo
done < $ROOT/$SEQLIST

echo "DEBUG: Sort file into GEO SEQ sort order."
sort $ROOT/$EXTEST > $ROOT/$EXTESTTR

echo "DEBUG: Combine across SEQ within GEO"
rm -f $ROOT/$EXTESTBG
while read -r geo; do
	grep "^${geo}," $ROOT/$EXTESTTR > $ROOT/tmpgeo2	
	/bin/echo -n "${geo}," >> $ROOT/$EXTESTBG
	cat $ROOT/tmpgeo2 \
		| cut -d, -f1,2 --complement \
		| tr '\054' '\012' \
		| sort -un \
		| tr '\012' '\054' \
		| sed 's/\,$//g' >> $ROOT/$EXTESTBG
	/bin/echo ""  >> $ROOT/$EXTESTBG
done < $ROOT/trbglist-small.txt
