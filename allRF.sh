#!/usr/bin/env bash
source setvars.sh
ADIR=$1

#Loop over rf-ace filter results and run fiedler and mds
for FILE in ${ADIR}/rf-ace/*
do
	echo Pairwise $FILE
	if [ -f $FILE ]
	then
		OUTDIRBASE=${ADIR}/rf-ace/layouts/$(basename $FILE)
		OUTDIR=${OUTDIRBASE}/fiedler
		if [ ! -d "$OUTDIR" ]; 
		then
			mkdir -p $OUTDIR
			
			./runpw.sh $FILE $OUTDIR 3
			RMEMPTY $OUTDIR
		fi

		OUTDIR=${OUTDIRBASE}/mds
		if [ ! -d "$OUTDIR" ]; 
		then
			mkdir -p $OUTDIR

			./runMDS.sh $FILE $OUTDIR 3
		fi
		RMEMPTY $OUTDIR
		RMEMPTY $OUTDIRBASE
	fi
done