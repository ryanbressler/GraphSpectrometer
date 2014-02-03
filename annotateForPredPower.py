
import os
import sys
import json
import branchMatrix
import numpy as np


def annotate(fn,fm,gestagefeature,cap1,cap2):
    print "Annotating %s with header from %s" % (os.path.abspath(fn), os.path.abspath(fm))

    fo = open(fn)
    data = json.load(fo)
    fo.close()

    fo = open(fm)
    colheaders = fo.next().rstrip().split("\t")[1:]
    rowheaders = []
    ptb = []
    termcat = []
    gestage = []

    for line in fo:
        vs = line.rstrip().split("\t")
        rowheaders.append(vs[0])
        if vs[0].startswith("B:CLIN:Preterm:NB::::"):
            ptb = vs[1:]
        if vs[0].startswith("N:CLIN:TermCategory:NB::::"):
            termcat = vs[1:]
        if vs[0].startswith(gestage):
            gestage = vs[1:]
    fo.close()

    #print "%s data points %s names%s colheaders %s rowheaders max %s" % (len(data["f1"]), len(data["nByi"]), len(colheaders), len(rowheaders), max((int(n) for n in data["nByi"])))
    #print json.dumps(colheaders)
    #print json.dumps(data["nByi"])
    nByi = [colheaders[int(n)] for n in data["nByi"]]
    data["nByi"] = nByi

    

    fmiByHeader = dict((key, value) for (value, key) in enumerate(colheaders))
    rank = dict((int(key), int(value)) for (value, key) in enumerate(data["r1"]))
    sortedi = np.array([rank[key] for key in sorted(rank.keys())])
    fmis = np.array([fmiByHeader[nByi[i]] for i in sortedi])
    
    data["ptb"] = list(np.array(ptb)[fmis])
    data["termcat"] = [int(float(n)) for n in list(np.array(termcat)[fmis])]
    data["gestage"] = [float(n) for n in list(np.array(gestage)[fmis])]
   
       

    for key in ["f1","f2","r1","r2","d","nByi"]:
        data[key] = list(np.array(data[key])[sortedi])

    data["iByn"] = dict((key, value) for (value, key) in enumerate(data["nByi"]))
    data["colorfeaturename"]=gestage
    data["cap1"]=cap1
    data["cap2"]=cap2

    print "Overwriting %s with version annotated for predpower vis" % (fn)
    fo = open(fn, "w")
    json.dump(data, fo, indent=2)
    fo.close()

def main():
    fn = sys.argv[1]
    fm = sys.argv[2]

    gestage = "N:CLIN:Gestational_Age_at_Delivery:NB::::"
    if len(sys.argv) == 3:
        annotate(fn,fm,gestagefeature,"Preterm  Preterm (PTB) vs. Fullterm (FTB)","Gestational Age (Weeks)")
    else:
        anotatefo = open(sys.argv[3])
        for line in anotatefo:
            vs = line.rstrip().split("\t")
            annotate(vs[3]+"/"+fn,fm,vs[1],vs[4],vs[2])
    

    


if __name__ == '__main__':
    main()