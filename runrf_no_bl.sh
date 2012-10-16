#!/usr/bin/env bash
FMATRIX=$1
OUTDIR=$2
NCORES=4
RFACE=/titan/cancerregulome9/workspaces/rf-ace/bin/rf-ace
GSPEC=/titan/cancerregulome9/workspaces/users/rbressle/GraphSpectrometer

cd $(OUTDIR)
echo RUNNING RANDOM FOREST WITH BLACKLIST
$RFACE -I $FMATRIX \
-i N:CLIN:TermCategory:NB:::: -O $(OUTDIR)/rf.pred.w.12800.unblacklisted.out -n 12800
echo PARSING PREDICTOR 
seq 0 1 60 | xargs --max-procs=16 -I CUTOFF  \
python $(GSPEC)/parseRfPred.py $(OUTDIR)/rf.pred.w.12800.unblacklisted.out CUTOFF
echo FINDING HODGE RANK
ls $(OUTDIR)/rf.pred.w.12800.unblacklisted.out*.json | xargs --max-procs=$(NCORES) -I FILE  \
python $(GSPEC)/plotpredDecomp.py FILE
