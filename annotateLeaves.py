
import os
import sys
import json
import branchMatrix
import numpy as np


def main():
    fn = sys.argv[1]
    fm = sys.argv[2]
    branches = sys.argv[3]

    print "Annotating %s with header from %s" % (os.path.abspath(fn), os.path.abspath(fm))

    fo = open(fn)
    data = json.load(fo)
    fo.close()

    fo = open(fm)
    colheaders = fo.next().rstrip().split("\t")[1:]
    rowheaders = []
    termcat = []
    for line in fo:
        vs = line.rstrip().split("\t")
        rowheaders.append(vs[0])
        if vs[0].startswith("N:CLIN:TermCategory:NB"):
            termcat = vs[1:]
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
    data["termcat"] = [int(n) for n in list(np.array(termcat)[fmis])]
    for key in ["f1","f2","r1","r2","d","nByi"]:
        data[key] = list(np.array(data[key])[sortedi])

    data["iByn"] = dict((key, value) for (value, key) in enumerate(data["nByi"]))

    print "Overwriting %s with version annotated for branch vis" % (fn)
    fo = open(fn, "w")
    json.dump(data, fo, indent=2)
    fo.close()
    
    fo = open(fn)
    data = json.load(fo)
    fo.close()

    data["branches"] = branchMatrix.branchMatrix(fn, fm, branches)

    print "Overwriting %s with version including branch data" % (fn)
    fo = open(fn, "w")
    json.dump(data, fo, indent=2)
    fo.close()


if __name__ == '__main__':
    main()