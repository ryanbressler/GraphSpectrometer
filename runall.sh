#!/usr/bin/env bash
ADIR=$1
BLACKLIST=$2
OUTDIRBASE=$3


#Loop over feature matrixes
for FILE in $(ADIR)/feature_matrices/*
do
	if [ -f $FILE ]
	then
		OUTDIR=$(OUTDIRBASE)/$(basename $FILE)
		if [ ! -e $OUTDIR ]
		then
			mkdir $OUTDIR
		fi
		bash runrf.sh $FILE $OUTDIR
		bash runrf_no_bl.sh $FILE $BLACKLIST $OUTDIR
	fi
done

#Loop over pairwise results
for FILE in $(ADIR)/pairwise/*
do
	if [ -f $FILE ]
	then
		OUTDIR=$(OUTDIRBASE)/$(basename $FILE)
		if [ ! -e $OUTDIR ]
		then
			mkdir $OUTDIR
		fi
		bash runpw.sh $FILE $OUTDIR
	fi
done
