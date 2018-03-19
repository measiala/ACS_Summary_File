#!/bin/sh

if test -x /usr/bin/python3;
	PYTHON3=/usr/bin/python3
elif test -x /usr/local/bin/python3
	PYTHON3=/usr/local/bin/python3

PYTHON3 $0
