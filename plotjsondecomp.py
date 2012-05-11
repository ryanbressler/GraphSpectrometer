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
from scipy.sparse.linalg import cg
from pydec import d, delta, simplicial_complex, read_mesh
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
		#scew symetricise
		A = (A.T - A)/2
		A=A.tocoo()
		pos=A.data>0

		sc = simplicial_complex(([[el] for el in range(0,A.shape[0])],numpy.column_stack((A.row[pos],A.col[pos])).tolist()))
		omega = sc.get_cochain(1)
		omega.v[:] = A.data[pos]
		p = omega.k
		alpha = sc.get_cochain(p - 1)
		#beta  = sc.get_cochain(p + 1)    

		# Solve for alpha
		A2 = delta(d(sc.get_cochain_basis(p - 1))).v
		b = delta(omega).v
		alpha.v = cg( A2, b, tol=1e-8 )[0]
		v = A.data[pos]-d(alpha).v
		cyclic_adj_list=numpy.column_stack((A.row[pos],A.col[pos],v)).tolist()
		div_adj_list=numpy.column_stack((A.row[pos],A.col[pos],d(alpha).v)).tolist()

		fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),cyclic_adj_list,fn+".decomp.cyclic.curl",widths=[64],vsdeg=False,nByi=data["nByi"],directed=True)
		fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),div_adj_list,fn+".decomp.acyclic.free",widths=[64],vsdeg=False,nByi=data["nByi"],directed=True)
		fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),data["adj"],fn+".decomp.acyclic.over.all.curl.",widths=[64],vsdeg=False,nByi=data["nByi"],adj_list2=div_adj_list,directed=True)

def main():
	fn=sys.argv[1]
	
	plotjson(fn)
	


if __name__ == '__main__':
	main()