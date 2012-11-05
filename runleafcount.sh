#!/usr/bin/env bash
source setvars.sh
ADIR=$1

#Loop over pairwise results and run fiedler and mds
for FMATRIX in ${ADIR}/feature_matrices/*
do
	echo Feature Matrix $FMATRIX
	FMNAME=$(basename $FMATRIX)
	for FILE in ${ADIR}/rf-pred/${FMNAME}*
	do
		NAME=$(basename $FILE)
		echo Feature Matrix $FMATRIX Predictor $FILE
		LEAFDIR=${ADIR}/rf-leaves
		BRANCHEDIR=${ADIR}/rf-branches
		mkdir -p $LEAFDIR
		mkdir -p $BRANCHEDIR

		BRANCHFILE=${BRANCHEDIR}/${NAME} 
		LEAFFILE=${LEAFDIR}/${NAME}
		${LCOUNT} -branches="$BRANCHFILE" -leaves="$LEAFFILE" \
		-rfpred="${FILE}" -fm="${FMATRIX}"
		if [ -e "${LEAFFILE}" ]
		then
			LEAFLAYOUT=${LEAFDIR}/layouts/${NAME}/fiedler
			if [ ! -d "$LEAFLAYOUT" ]; 
			then

				mkdir -p $LEAFLAYOUT
				cd $LEAFLAYOUT
				seq 2 2 128 | xargs -P 8 -I CUT python ${GSPEC}/fiedler.py ${LEAFFILE} CUT
				for JSONFILE in ${LEAFLAYOUT}/*
				do
					python ${GSPEC}/annotateLeaves.py $JSONFILE $FMATRIX 
				done

				cd -
			fi
			RMEMPTY $LEAFLAYOUT
			RMEMPTY ${LEAFDIR}/layouts/${NAME}
		fi
		RMEMPTY ${LEAFDIR}/layouts 
		RMEMPTY $LEAFDIR
		RMEMPTY $BRANCHEDIR

		


	done
done