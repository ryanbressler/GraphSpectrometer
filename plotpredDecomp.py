"""
plotjsondecomp.py

Script to make plots from json files calculated by fiedler.py including an acyclic component

usage:

python plotjsondecomp.python fiedler.out.json

or often:
ls *.json | xargs --max-procs=10 -I FILE  python plotjsondecomp.py FILE

"""

import sys
import json
import numpy
from numpy import asarray, eye, outer, inner, dot, vstack
from numpy.random import seed, rand
from numpy.linalg import norm
from scipy.sparse.linalg import cg, lsqr
import scipy.sparse
from pydec import d, delta, simplicial_complex, abstract_simplicial_complex
import fiedler

def plotjson(fn):
    """
    plotjson: make plots from json output of fiedler.py

    fn: the filename of the json file
    """

    fo=open(fn)
    data=json.load(fo)
    fo.close()
    if "adj" in data:
        (A,adj,Npts) = fiedler.adj_mat(data["adj"])

        A =  A
        pos=A.data>0


        #A = (A.T - A)/2

        A=A.tocoo()
        pos=A.data>0
        skew = numpy.column_stack((A.row[pos],A.col[pos],A.data[pos])).tolist()
        
      
        # method from ranking driver.py
    
        asc = abstract_simplicial_complex([numpy.column_stack((A.row[pos],A.col[pos])).tolist()])
        B1 = asc.chain_complex()[1] # boundary matrix
        rank = lsqr(B1.T, A.data[pos])[0] # solve least squares problem
        
        sc = simplicial_complex(([[el] for el in range(0,A.shape[0])],numpy.column_stack((A.row[pos],A.col[pos])).tolist()))
        omega = sc.get_cochain(1)
        omega.v[:] = A.data[pos]
        p = omega.k
        alpha = sc.get_cochain(p - 1)
        
        alpha.v = rank
        v = A.data[pos]-d(alpha).v
        
        cyclic_adj_list=numpy.column_stack((A.row[pos],A.col[pos],v)).tolist()
        div_adj_list=numpy.column_stack((A.row[pos],A.col[pos],d(alpha).v)).tolist()

        data["hodge"]=list(rank)
        data["hodgerank"]=list(numpy.argsort(numpy.argsort(rank)))
        fo = open(fn,"w")
        json.dump(data,fo, indent=2)
        fo.close()
        A.data = A.data * .25
        alist=fiedler.adj_list(A)
        fn=fn+".abstract"
        #fiedler.doPlots(numpy.array(data["f1"]),-1*numpy.array(rank),numpy.array(data["d"]),alist,fn+".all.v.grad.",widths=[24],heights=[6],vsdeg=False,nByi=data["nByi"],directed=False)
        fiedler.doPlots(numpy.argsort(numpy.argsort(numpy.array(data["f1"]))),-1*numpy.log(numpy.array(rank)-numpy.amin(rank)+1),numpy.array(data["d"]),alist,fn+"fied.rank.v.hodge",widths=[24],heights=[16],vsdeg=False,nByi=data["nByi"],directed=False,dorank=False)
        
        

def main():
    fn=sys.argv[1]
    
    plotjson(fn)
    


if __name__ == '__main__':
    main()