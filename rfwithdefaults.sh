#!/usr/bin/env bash
#uusage: ls */folds/*/train*.fm | xargs -P 8 -I FILE bash /titan/cancerregulome9/ITMI_PTB/bin/GraphSpectrometer/rfwithdefaults.sh FILE
RFACE=/titan/cancerregulome9/ITMI_PTB/bin/rf-ace-read-only/bin/rf-ace
FMATRIX=$1
OUTDIR=$(pwd)
TARGET=B:CLIN:Preterm:NB::::
NAME=$(basename $FMATRIX)
MTRY=$(wc -l  $FMATRIX | awk 'END {print int(sqrt($1))}')

TREES=${FMATRIX}.sf

cd ${OUTDIR}

echo RUNNING RANDOM FOREST
echo RFACE $RFACE
echo FMATRIX $FMATRIX
echo TREES $TREES
echo TARGET $TARGET
echo MTRY $MTRY
$RFACE -I $FMATRIX \
-i $TARGET \
--nTrees  2500 \
--mTry ${MTRY} \
--nodeSize 1 \
--saveForest ${TREES}


