#!/usr/bin/env bash
#ls */folds/*/test*.fm | xargs -P 8 -I FILE bash /titan/cancerregulome9/ITMI_PTB/bin/GraphSpectrometer/errorrate.sh FILE
TESTFILE=$1
FILE=$(basename $TESTFILE)
FORREST=${TESTFILE//test/train}.sf
ERROR=$($GOPATH/bin/errorrate -fm ${TESTFILE} -rfpred ${FORREST})
echo ${FILE}	${ERROR}