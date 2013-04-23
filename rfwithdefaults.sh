#!/usr/bin/env bash
RFACE=/titan/cancerregulome9/ITMI_PTB/bin/rf-ace-read-only/bin/rf-ace
FMATRIX=$1
OUTDIR=$(pwd)
TARGET=B:CLIN:Preterm:NB::::
NAME=$(basename $FMATRIX)
NROWS=$(wc -l $FMATRIX)
MTRY=$(echo "sqrt($NROWS-1)" | bc -l)

TREES=${OUTDIR}/${NAME}.sf

cd ${OUTDIR}
if [ ! -e "$TREES" ]; 
then
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
	--saveForest ${TREES}
fi

