#!/usr/bin/env bash
FMATRIX=$1
BLACKLIST=$2
OUTDIR=$3

cd $(OUTDIR)
echo RUNNING RANDOM FOREST WITH BLACKLIST
$RFACE -I $FMATRIX \
-i N:CLIN:TermCategory:NB:::: -B $(BLACKLIST) -O $(OUTDIR)/rf.pred.w.12800.blacklisted.out -n 12800
echo PARSING PREDICTOR AND FINDING FIEDLER VECTORS
seq 0 1 60 | xargs --max-procs=$(NGSPECCORES) -I CUTOFF  \
python $(GSPEC)/parseRfPred.py $(OUTDIR)/rf.pred.w.12800.blacklisted.out CUTOFF
echo FINDING HODGE RANK
ls $(OUTDIR)/rf.pred.w.12800.blacklisted.out*.json | xargs --max-procs=$(NGSPECPLOTINGCORES) -I FILE  \
python $(GSPEC)/plotpredDecomp.py FILE


