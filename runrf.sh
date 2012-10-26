#!/usr/bin/env bash
FMATRIX=$1
BLACKLIST=$2
OUTDIR=$3
NAME=$(basename $FMATRIX)
TREES=${OUTDIR}/${NAME}_blacklisted

cd ${OUTDIR}
echo RUNNING RANDOM FOREST WITH BLACKLIST
$RFACE -I $FMATRIX \
-i N:CLIN:TermCategory:NB:::: -B ${BLACKLIST} -O ${TREES} -n 12800

OUTDIR=${OUTDIR}/layouts/$(basename $TREES)
if [ ! -e $OUTDIR ]
then
	mkdir $OUTDIR
fi

cd ${OUTDIR}
echo PARSING PREDICTOR 
seq 0 1 60 | xargs --max-procs=NGSPECCORES -I CUTOFF  \
python ${GSPEC}/parseRfPred.py ${TREES} CUTOFF
echo FINDING HODGE RANK
ls ${OUTDIR}/* | xargs --max-procs=${NGSPECPLOTINGCORES} -I FILE  \
python ${GSPEC}/plotpredDecomp.py FILE



