#!/usr/bin/env bash
source setvars.sh

FMATRIX=$1
INDIR=$2
OUTDIR=$3
TREES=$(ls ${INDIR}/rf2_*_31.sf| paste -s -d ',')

set +e
cd ${OUTDIR}



JSONDIR=${OUTDIR}/layouts/$(basename $TREES)/hodge


mkdir -p $JSONDIR
if [ -e "${TREES}" ]
then


	echo Feature Matrix $FMATRIX Predictor $TREES
	LEAFDIR=${ADIR}/rf-leaves
	BRANCHEDIR=${ADIR}/rf-branches
	BRANCHEMATDIR=${ADIR}/rf-branch-matrix

	mkdir -p $LEAFDIR
	mkdir -p $BRANCHEDIR
	mkdir -p $BRANCHEMATDIR

	BRANCHFILE=${OUTDIR}/branchfile 
	BRANCHMATFILE=${OUTDIR}/branchmatfile 
	LEAFFILE=${OUTDIR}/leaffile
	${LCOUNT} -branches="${BRANCHFILE}" -leaves="${LEAFFILE}" \
	-rfpred="${TREES}" -fm="${FMATRIX}"
	
	if [ -e $LEAFFILE ] 
	then	
					
		xargs -P ${NPYCORES} -I CUT python ${GSPEC}/parseByCol.py ${LEAFFILE} 0 2

		python ${GSPEC}/annotateLeaves.py $JSONFILE $FMATRIX $BRANCHFILE $TARGET
		

		python ${GSPEC}/branchMatrix.py $JSONFILE $FMATRIX $BRANCHFILE $BRANCHMATFILE
			
		
	fi
	
fi
