#!/usr/bin/env bash
# usage ./runall.sh /titan/cancerregulome9/ITMI_PTB/public/analysis/ /titan/cancerregulome9/workspaces/users/rbressle/2012_09_18/blacklist.txt /titan/cancerregulome9/ITMI_PTB/public/analysis/layouts/
source setvars.sh
ADIR=$1
BLACKLIST=$2


bash ${GSPEC}/allRFPred.sh $1 $2

bash ${GSPEC}/allPW.sh $1

bash ${GSPEC}/allRF.sh $1

bash ${GSPEC}/runleadcount.sh $1




