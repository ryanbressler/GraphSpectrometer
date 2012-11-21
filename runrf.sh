#!/usr/bin/env bash
source setvars.sh

FMATRIX=$1
BLACKLIST=$2
OUTDIR=$3
NAME=$(basename $FMATRIX)
TREES=${OUTDIR}/${NAME}_blacklisted
set +e
cd ${OUTDIR}
if [ ! -e "$TREES" ]; 
then
	echo RUNNING RANDOM FOREST WITH BLACKLIST
	$RFACE -I $FMATRIX \
	 --featureWeights ${BLACKLIST} -S ${TREES} $RFACEOPTIONS
fi

JSONDIR=${OUTDIR}/layouts/$(basename $TREES)/hodge
mkdir -p $JSONDIR
if [ ! -d "$JSONDIR" ]; 
then
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


