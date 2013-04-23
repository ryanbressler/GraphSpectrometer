#!/usr/bin/env bash
TESTFILE = $1
FORREST = ${TESTFILE//test/train}.sf
ERROR = $($GOPATH/bin/errorrate -fm ${TESTFILE} -rfpred ${FORREST})
echo $TESTFILE\t$ERROR