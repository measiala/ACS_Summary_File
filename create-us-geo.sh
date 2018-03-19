#!/bin/bash

ROOT=./data
GEOROOT=./geo

rm -f $ROOT/g20145.csv
find $GEOROOT -name "g20145[a-z][a-z].csv" -print | sort | xargs -I'{}' cat {} \
	| ./create-us-geo.awk >> $ROOT/g20145.csv
