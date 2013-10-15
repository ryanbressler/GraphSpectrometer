#!/usr/bin/env bash
export GSPEC=/titan/cancerregulome9/ITMI_PTB/bin/GraphSpectrometer

FMATRIX=$1
INDIR=$2
OUTDIR=$INDIR
TARGET=$3
TREES=$(ls ${INDIR}/rf1_*_31.sf| paste -s -d ',')


cd ${OUTDIR}


echo Feature Matrix $FMATRIX Predictor $TREES

BRANCHFILE=${OUTDIR}/branchfile 
BRANCHMATFILE=${OUTDIR}/branchmatfile 
LEAFFILE=${OUTDIR}/leaffile

leafcount -branches="${BRANCHFILE}" -leaves="${LEAFFILE}" \
-rfpred="${TREES}" -fm="${FMATRIX}"

if [ -e $LEAFFILE ] 
then	
				
	python ${GSPEC}/parseByCol.py ${LEAFFILE} 0 2

	JSONFILE=${LEAFFILE}.cutoff.0.0.json

	python ${GSPEC}/annotateLeaves.py $JSONFILE $FMATRIX $BRANCHFILE $TARGET
	

	python ${GSPEC}/branchMatrix.py $JSONFILE $FMATRIX $BRANCHFILE $BRANCHMATFILE
		
	
fi
	

