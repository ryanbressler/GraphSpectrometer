#!/usr/bin/env bash
source setvars.sh

FMATRIX=$1
OUTDIR=$2
NAME=$(basename $FMATRIX)
TREES=${OUTDIR}/${NAME}_unblacklisted
set +e

cd ${OUTDIR}
if [ ! -e "$TREES" ]; 
then
	echo RUNNING RANDOM FOREST
	echo RFACE $RFACE
	echo FMATRIX $FMATRIX
	echo TREES $TREES
	$RFACE -I $FMATRIX \
	--saveForest ${TREES} $RFACEOPTIONS
fi


JSONDIR=${OUTDIR}/layouts/$(basename $TREES)/hodge
if [ ! -d "$JSONDIR" ]; 
then
	mkdir -p $JSONDIR


	if [ -e "${TREES}" ]
	then
		cd ${JSONDIR}
		echo PARSING PREDICTOR 
		seq 0 1 60 | xargs --max-procs=${NGSPECCORES} -I CUTOFF  \
		python ${GSPEC}/parseRfPred.py ${TREES} CUTOFF
		echo FINDING HODGE RANK
		ls ${JSONDIR}/* | xargs --max-procs=${NGSPECPLOTINGCORES} -I FILE  \
		python ${GSPEC}/plotpredDecomp.py FILE
	fi
fi
set -e

cd ${OUTDIR}
RMEMPTY $JSONDIR
RMEMPTY ${OUTDIR}/layouts/$(basename $TREES)
