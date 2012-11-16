
import os
import sys


def main():
    fn = sys.argv[1]
    fm = sys.argv[2]

    print "Filtering %s with  %s" % (os.path.abspath(fn), os.path.abspath(fm))

    fo = open(fm)
    termcat = []
    for line in fo:
        vs = line.rstrip().split("\t")
        if vs[0].startswith("N:CLIN:TermCategory:NB"):
            termcat = vs[1:]
    fo.close()

    preterm = []
    fset = frozenset(["1", "2", "3"])
    for i, v in termcat:
        if v in fset:
            preterm.append(i)
    preterm = frozenset(preterm)
    
    fin = open(fn)
    fout = open(fn + "_preterm", "w")

    for line in fin:
        vs = line.rstrip().split()
        if int(vs[0]) in preterm and int(vs[1]) in preterm:
            fout.write(line)
    fin.close()
    fout.close()



if __name__ == '__main__':
    main()