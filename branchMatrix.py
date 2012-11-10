
import os
import sys
import json
import collections




def main():
    print "Geberating branch matrix using  %s %s %s %s"%(os.path.abspath(fn),os.path.abspath(fm),branches,branchmatrix)

    fn = sys.argv[1]
    fm = sys.argv[2]
    branches=sys.argv[3]
    branchmatrix=sys.argv[4]

    fo=open(fn)
    data=json.load(fo)
    fo.close()

    fo=open(fm)
    colheaders=fo.next().rstrip().split("\t")[1:]
    rowheaders=[]
    for line in fo:
        rowheaders.append(line.rstrip().split("\t")[0])


    counters = []
    for i,v in enumerate(colheaders):
        counters.append(collections.Counter())
    fo = open(branches)
    for line in fo:
        vs = [int(v) for v in line.rstrip().split("\t")]
        counters[vs[0]][vs[1]]+= vs[2]
    fo.close()
    fmiByHeader=dict((key, value) for (value, key) in enumerate(colheaders))
    rank = dict((int(key), int(value)) for (value, key) in enumerate(data["r1"]))
    sortedkeys = sorted(rank.keys())

    colheaders = []
    colindexes = []

    for key in sortedkeys:
        name = data["nByi"][rank[key]]
        colheaders.append(name)
        colindexes.append(fmiByHeader[name])

    print "Outputing branchmatirx to %s from %s and %s"%(branchmatrix,fm,branches)
    fo = open(branchmatrix,"w")
    fo.write("feature\t%s\n"%("\t".join(colheaders)))


    for fi, feature in enumerate(rowheaders):
        vs=[feature]
        for ci in colindexes:
            vs.append(str(counters[ci][fi]))
        fo.write("%s\n"%("\t".join(vs)))
    fo.close()


if __name__ == '__main__':
    main()