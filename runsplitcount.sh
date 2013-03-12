#!/usr/bin/env bash
source setvars.sh
export SPLITCOUNT=/titan/cancerregulome9/ITMI_PTB/bin/go/src/github.com/rbkreisberg/CloudForest/splitcount/splitcount
ADIR=$1

#Loop over pairwise results and run fiedler and mds
for FMATRIX in ${ADIR}/../domains/feature_matrices/*
do
  	echo Feature Matrix $FMATRIX
        FMNAME=$(basename $FMATRIX)
        for FILE in ${ADIR}/rf-pred/${FMNAME}*
        do
          	NAME=$(basename $FILE)
                echo Feature Matrix $FMATRIX Predictor $FILE
                SPLITDIR=${ADIR}/rf-splits
                BRANCHEDIR=${ADIR}/rf-splits-branches
                BRANCHEMATDIR=${ADIR}/rf-splits-relbranches
                SPLITLISTDIR=${ADIR}/rf-splits-lists

                mkdir -p $SPLITDIR
                mkdir -p $BRANCHEDIR
                mkdir -p $BRANCHEMATDIR
                mkdir -p $SPLITLISTDIR

                BRANCHFILE=${BRANCHEDIR}/${NAME}
                RELBRANCHFILE=${BRANCHEMATDIR}/${NAME}
                SPLITFILE=${SPLITDIR}/${NAME}
                SPLITLISTFILE=${SPLITLISTDIR}/${NAME}
                ${SPLITCOUNT} -branches="$BRANCHFILE" -splits="$SPLITFILE" -relbranches="$RELBRANCHFILE" -splitlist="$SPLITLISTFILE"\
                -rfpred="${FILE}" -fm="${FMATRIX}"

        done
done
