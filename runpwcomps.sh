#!/usr/bin/env bash
# usage ./runpwcomps.sh files*.pwpv
export NGSPECCORES=4
export NGSPECPLOTINGCORES=2
export GSPEC=/titan/cancerregulome9/ITMI_PTB/bin/GraphSpectrometer

#for FILE in /titan/cancerregulome3/TCGA/outputs/brca/brca.newMerge.01oct.hack.imp1_NCI.*.pwpv
#do
#	grep GNAB $FILE > $(basename $FILE)
#done

for PWFILE in "$@"
do
	seq .8 -.2 .2 | xargs --max-procs=${NGSPECCORES} -I CUTOFF  \
	python ${GSPEC}/fiedler.py \
	${PWFILE} CUTOFF
done

seq .8 -.2 .2 | xargs --max-procs=${NGSPECPLOTINGCORES} -I ${CUTOFF}  \
python ${GSPEC}/comparisonPlot.py "*.pwpv${CUTOFF}.continuous.json"

