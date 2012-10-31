#!/usr/bin/env bash
source setvars.sh
ADIR=$1
BLACKLIST=$2

#Loop over feature matrixes and run and layout rf-ace predictors
for FILE in ${ADIR}/feature_matrices/*
do
	echo Feature Matrix $FILE
	if [ -f $FILE ]
	then
		OUTDIRBASE=${ADIR}/rf-pred/
		LAYOUTS=${OUTDIRBASE}/layouts
		mkdir -p $LAYOUTS
		

		./runrf_no_bl.sh $FILE $OUTDIRBASE
		./runrf.sh $FILE $BLACKLIST $OUTDIRBASE
	fi
done