#!/usr/bin/env bash
source setvars.sh
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
		LEAFDIR=${ADIR}/rf-leaves
		BRANCHEDIR=${ADIR}/rf-branches
		BRANCHEMATDIR=${ADIR}/rf-branch-matrix

		mkdir -p $LEAFDIR
		mkdir -p $BRANCHEDIR
		mkdir -p $BRANCHEMATDIR

		BRANCHFILE=${BRANCHEDIR}/${NAME} 
		BRANCHMATFILE=${BRANCHEMATDIR}/${NAME} 
		LEAFFILE=${LEAFDIR}/${NAME}
		${LCOUNT} -branches="$BRANCHFILE" -leaves="$LEAFFILE" \
		-rfpred="${FILE}" -fm="${FMATRIX}"
		if [ -e $LEAFFILE] 
		then	
			python ${GSPEC}/pruneLeaves.py $LEAFFILE $FMATRIX

			for INERRFILE in ${LEAFFILE}*
			do
				INNERNAME=$(basename INERRFILE)
				LEAFLAYOUT=${LEAFDIR}/layouts/${INNERNAME}/fiedler
				#if [ ! -d "$LEAFLAYOUT" ]; 
				#then

					mkdir -p $LEAFLAYOUT
					cd $LEAFLAYOUT
					seq 0 2 0 | xargs -P 8 -I CUT python ${GSPEC}/parseByCol.py ${INERRFILE} CUT 2
					for JSONFILE in ${LEAFLAYOUT}/*
					do
						python ${GSPEC}/annotateLeaves.py $JSONFILE $FMATRIX $BRANCHFILE
					done

					cd -
				#fi
				RMEMPTY $LEAFLAYOUT
				RMEMPTY ${LEAFDIR}/layouts/${INNERNAME}
				JSONFILE=${LEAFLAYOUT}/${INNERNAME}.cutoff.0.0.json
				python ${GSPEC}/branchMatrix.py $JSONFILE $FMATRIX $BRANCHFILE $BRANCHMATFILE
				
			done
		fi
		RMEMPTY ${LEAFDIR}/layouts 
		RMEMPTY $LEAFDIR
		RMEMPTY $BRANCHEDIR
		RMEMPTY $BRANCHEMATDIR

		


	done
done