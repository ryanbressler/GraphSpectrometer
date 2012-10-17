#!/usr/bin/env bash
# usage ./runall.sh /titan/cancerregulome9/ITMI_PTB/public/analysis/ /titan/cancerregulome9/workspaces/users/rbressle/2012_09_18/blacklist.txt /titan/cancerregulome9/ITMI_PTB/public/analysis/layouts/
ADIR=$1
BLACKLIST=$2
OUTDIRBASE=$3


#Loop over feature matrixes
for FILE in $(ADIR)/feature_matrices/*
do
	echo Feature Matrix $FILE
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
	echo Pairwise $FILE
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
