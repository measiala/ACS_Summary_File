#!/bin/sh

if [ $# -lt 2 ]||[ "$1" = "-h" ]||[ "$1" = "--help" ]; then
    exec >&2
    echo "Usage: $0 [ -h | --help ]"
    echo "       $0 YYYY PER"
    echo "Where:"
    echo "       YYYY is equal to the 4-digit end year of the data set."
    echo "       PER is equal to the period (1/5) of the data set (1-year or 5-year)."
    echo ""
    exit 3
fi

if [ $1 -ge 2005 ]&&[ $1 -le 2016 ]; then
    YYYY=$1
else
    exec >&2
    echo "The value of YYYY = $YYYY is out of range."
    exit 3
fi

if [ "$2" -eq "1" ]||[ "$2" -eq "3" ]||[ "$2" -eq "5" ]; then
    PER=$2
else
    exec >&2
    echo "The value of PER = $PER is out of range."
fi

echo "YYYY=$YYYY PER=$PER"

ARCHPATH=./webarchive/${YYYY}/${PER}
GEOPATH=./geo/${YYYY}/${PER}
DATAPATH=./data/${YYYY}/${PER}
INPUTPATH=./input/${YYYY}/${PER}

mkdir -p "$ARCHPATH"
mkdir -p "$GEOPATH"
mkdir -p "$DATAPATH"
mkdir -p "$INPUTPATH"

if [ $PER = "5" ]; then
    INGEOFILE=${YYYY}_ACS_Geography_Files.zip
    ZIPDIR=geo/
elif [ $PER = "1" ]; then
    INGEOFILE=All_Geographies.zip
    ZIPDIR=
fi
INTBLFILE=ACS_${PER}yr_Seq_Table_Number_Lookup.txt
OUTGEOFILE=ACS_${YYYY}_${PER}_Year_ACS_Geography_Files.zip
OUTTBLFILE=ACS_${YYYY}_${PER}_Year_Seq_Table_Number_Lookup.txt

echo "https://www2.census.gov/programs-surveys/acs/summary_file/${YYYY}/data/${PER}_year_entire_sf/$INGEOFILE"

wget -nc -O $ARCHPATH/$OUTGEOFILE \
     https://www2.census.gov/programs-surveys/acs/summary_file/${YYYY}/data/${PER}_year_entire_sf/$INGEOFILE

unzip -naLj -d $GEOPATH $ARCHPATH/$OUTGEOFILE ${ZIPDIR}g${YYYY}${PER}??.csv

echo "https://www2.census.gov/programs-surveys/acs/summary_file/${YYYY}/documentation/user_tools/$INTBLFILE"

wget -nc -O $ARCHPATH/$OUTTBLFILE \
     https://www2.census.gov/programs-surveys/acs/summary_file/${YYYY}/documentation/user_tools/$INTBLFILE

if [ -r "./webarchive/${YYYY}/g${YYYY}.lay" ]; then
    cat ./webarchive/${YYYY}/g${YYYY}.lay | tr '\012' ',' | sed 's/,$//g' > ./geo/${YYYY}/g${YYYY}.lay
fi
