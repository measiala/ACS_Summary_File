#!/bin/sh

tar xvf Tracts_Block_Groups_Only.tar `grep -e 'e20145' sumfile-list.txt | grep -E '0001|010[2-9]|011[0-1]'`
