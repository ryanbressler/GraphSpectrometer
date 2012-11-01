
import os
import sys
import json



        

def main():
    fn=sys.argv[1]
    fm=sys.argv[2]
    print "Annotating %s with header from %s"%(os.path.abspath(fn),os.path.abspath(fm))

    fo=open(fn)
    data=json.load(fo)
    fo.close()

    fo=open(fm)
    data["nByi"]=fo.readline().rstrip().split("\t")[1:]
    data["iByn"]=dict((key, value) for (value, key) in enumerate(data["nByi"]))
    fo.close()

    print "Overwriting %s with annotated version."%(fn)
    fo = open(fn,"w")
    json.dump(data,fo, indent=2)
    fo.close()
    


if __name__ == '__main__':
    main()