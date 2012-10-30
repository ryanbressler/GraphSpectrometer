#!/usr/bin/env bash
FMATRIX=$1
OUTDIR=$2
NAME=$(basename $FMATRIX)
TREES=${OUTDIR}/${NAME}_unblacklisted

cd ${OUTDIR}
echo RUNNING RANDOM FOREST WITH BLACKLIST
$RFACE -I $FMATRIX \
-i N:CLIN:TermCategory:NB:::: -O ${TREES} -n 12800

JSONDIR=${OUTDIR}/layouts/$(basename $TREES)/hodge

mkdir -p $JSONDIR


cd ${JSONDIR}
echo PARSING PREDICTOR 
seq 0 1 60 | xargs --max-procs=NGSPECCORES -I CUTOFF  \
python ${GSPEC}/parseRfPred.py ${TREES} CUTOFF
echo FINDING HODGE RANK
ls ${JSONDIR}/* | xargs --max-procs=${NGSPECPLOTINGCORES} -I FILE  \
python ${GSPEC}/plotpredDecomp.py FILE

if [ "$(ls -A $JSONDIR)" ]; then
     echo "$JSONDIR is not Empty"
else
    echo "$JSONDIR is Empty. Removeing."
    rm $JSONDIR
fi
