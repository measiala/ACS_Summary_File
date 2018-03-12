#!/bin/awk -f

BEGIN{
	FS=","
}
{
	printf "%s,",tolower($3)$6;

	for (i=1;i<6;i++) {
		printf "%s,",$i;
	}

	for (i=7;i<NF;i++) {
		printf "%s,",$i;
	}

	print $NF;
}
END{
}
