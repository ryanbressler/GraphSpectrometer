#!/usr/bin/env bash
# usage ./runall.sh /titan/cancerregulome9/ITMI_PTB/public/analysis/ /titan/cancerregulome9/workspaces/users/rbressle/2012_09_18/blacklist.txt /titan/cancerregulome9/ITMI_PTB/public/analysis/layouts/
export NGSPECCORES=4
export GSPEC=/titan/cancerregulome9/workspaces/users/rbressle/GraphSpectrometer

for FILE in /titan/cancerregulome3/TCGA/outputs/brca/brca.newMerge.01oct.hack.imp1_NCI.*.pwpv
do
	grep GNAB $FILE > $(basename $FILE)
done

ls *.pwpv | xargs --max-procs=${NGSPECCORES} -I FILE  python ${GSPEC}/fiedler.py FILE

python ${GSPEC}/comparisonPlot.py "*.pwpv.json"

