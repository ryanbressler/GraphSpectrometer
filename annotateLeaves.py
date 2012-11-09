
import os
import sys
import json
import collections



        

def main():
    fn=sys.argv[1]
    fm=sys.argv[2]
    branches=sys.argv[3]
    branchmatrix=sys.argv[4]
    print "Annotating %s with header from %s"%(os.path.abspath(fn),os.path.abspath(fm))

    fo=open(fn)
    data=json.load(fo)
    fo.close()

    fo=open(fm)
    colheaders=fo.next().rstrip().split("\t")[1:]
    rowheaders=[]
    for line in fo:
        rowheaders.append(line.rstrip().split("\t")[0])

    print "%s "

    nByi=[colheaders[int(n)] for n in data["nByi"]]
    data["nByi"]= nByi
    data["iByn"]=dict((key, value) for (value, key) in enumerate(data["nByi"]))
    fo.close()

    print "Overwriting %s with annotated version."%(fn)
    fo = open(fn,"w")
    json.dump(data,fo, indent=2)
    fo.close()

    counters = []
    for i,v in enumerate(colheaders):
        counters.append(Counter())
    fo = open(brances)
    for line in fo:
        vs = [int(v) for v in line.rstrip().split("\t")]
        counters[vs[0]][vs[1]]+= vs[2]
    fo.close()

    print "Outputing branchmatirx to %s from %s and %s"%(branchmatirx,fm,branches)
    fo = open(branchmatrix,"w")
    fo.write("feature\t%s\n"%("\t".join(colheaders)))
    

    for fi, feature in enumerate(rowheaders):
        vs=[feature]
        for ci, case in enumerate(colheaders):
            vs.append(str(counters[ci][fi]))
        fo.write("%s\n"%("\t".join(vs)))
    fo.close()




    


if __name__ == '__main__':
    main()