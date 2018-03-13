#!/bin/sh

if [ $# -lt 2 ]||[ "$1" == "-h" ]||[ "$1" == "--help" ]; then
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

mkdir -p "./webarchive"
mkdir -p "./geo"
mkdir -p "./data"
mkdir -p "./input"

if [ $PER == "5" ]; then
    GEOFILE=${YYYY}_ACS_Geography_Files.zip
    OUTFILE=${YYYY}_${PER}_Year_ACS_Geography_Files.zip
    ZIPDIR=geo/
    GEODIR=./
elif [ $PER == "1" ]; then
    GEOFILE=All_Geographies.zip
    OUTFILE=
    ZIPDIR=
    GEODIR=./geo
fi
OUTFILE=${YYYY}_${PER}_Year_ACS_Geography_Files.zip
LKUPFILE=ACS_${PER}yr_Seq_Table_Number_Lookup.txt

wget -nc -O ./webarchive/$OUTFILE https://www2.census.gov/programs-surveys/acs/summary_file/${YYYY}/data/${PER}_year_entire_sf/$GEOFILE

unzip -naL -d $GEODIR ./webarchive/$OUTFILE ${ZIPDIR}g${YYYY}${PER}??.csv

wget -nc -O ./webarchive/$LKUPFILE https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/$LKUPFILE
