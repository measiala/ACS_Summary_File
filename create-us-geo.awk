#!/bin/awk -f

BEGIN{
	FS=","
}
{
	printf "%s,%s,%s,",tolower($2)$5,$3,$4;

	for (i=6;i<NF;i++) {
		printf "%s,",$i;
	}

	print $NF;
}
END{
}
