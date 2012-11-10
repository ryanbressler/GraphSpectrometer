
import os
import sys
import json


def main():
    fn = sys.argv[1]
    fm = sys.argv[2]

    print "Annotating %s with header from %s"%(os.path.abspath(fn),os.path.abspath(fm))

    fo=open(fn)
    data=json.load(fo)
    fo.close()

    fo=open(fm)
    colheaders=fo.next().rstrip().split("\t")[1:]
    rowheaders=[]
    for line in fo:
        rowheaders.append(line.rstrip().split("\t")[0])

    print "%s data points %s names%s colheaders %s rowheaders max %s"%(len(data["f1"]),len(data["nByi"]),len(colheaders),len(rowheaders),max((int(n) for n in data["nByi"])))
    #print json.dumps(colheaders)
    #print json.dumps(data["nByi"])
    nByi=[colheaders[int(n)] for n in data["nByi"]]
    data["nByi"]= nByi
    data["iByn"]=dict((key, value) for (value, key) in enumerate(data["nByi"]))
    fo.close()

    print "Overwriting %s with annotated version."%(fn)
    fo = open(fn,"w")
    json.dump(data,fo, indent=2)
    fo.close()



if __name__ == '__main__':
    main()