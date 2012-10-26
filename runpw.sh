#!/usr/bin/env bash
#This will only work if the input file has .pwpv exstension
PWFILE=$1
OUTDIR=$2


#fnbase=2012_09_19.pwpv

cd ${OUTDIR}
echo PARSIN PWFILE AND FINDING FIEDLER VECTORS
seq 1 -.1 0 | xargs --max-procs=${NGSPECCORES} -I CUTOFF  \
python ${GSPEC}/fiedler.py \
${PWFILE} CUTOFF
# echo PLOTTING PWFILE FIEDLER VECTORS
# ls *.pwpv.json | xargs --max-procs=${NGSPECPLOTINGCORES} -I FILE  \
# python ${GSPEC}/plotjson.py FILE
