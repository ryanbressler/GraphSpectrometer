#!/usr/bin/env bash
export GSPEC=/titan/cancerregulome9/ITMI_PTB/bin/GraphSpectrometer

FMATRIX=$1
INDIR=$2
OUTDIR=$INDIR
TREES=$(ls ${INDIR}/rf1_*_31.sf| paste -s -d ',')


cd ${OUTDIR}


echo Feature Matrix $FMATRIX Predictor $TREES

BRANCHFILE=${OUTDIR}/branchfile 
BRANCHMATFILE=${OUTDIR}/branchmatfile 
LEAFFILE=${OUTDIR}/leaffile

leafcount -leaves="${LEAFFILE}" \
-rfpred="${TREES}" -fm="${FMATRIX}" -threads 2

if [ -e $LEAFFILE ] 
then	
				
	python ${GSPEC}/parseByCol.py ${LEAFFILE} 0 2

	JSONFILE=${LEAFFILE}.cutoff.0.0.json

	python ${GSPEC}/annotateForPredPower.py $JSONFILE $FMATRIX
		
	
fi
	

