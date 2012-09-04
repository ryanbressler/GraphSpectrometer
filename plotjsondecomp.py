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
		#scew symetricise
		A = (A.T - A)/2
		A=A.tocoo()
		
		pos=A.data>0
		skew = numpy.column_stack((A.row[pos],A.col[pos],A.data[pos])).tolist()
		
		# #method from hodge decomposition driver.py
		# sc = simplicial_complex(([[el] for el in range(0,A.shape[0])],numpy.column_stack((A.row[pos],A.col[pos])).tolist()))
		# omega = sc.get_cochain(1)
		# omega.v[:] = A.data[pos]
		# p = omega.k
		# alpha = sc.get_cochain(p - 1)
		# #beta  = sc.get_cochain(p + 1)    

		# # Solve for alpha
		# A2 = delta(d(sc.get_cochain_basis(p - 1))).v
		# b = delta(omega).v
		# rank=cg( A2, b, tol=1e-8 )[0]

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

		fn=fn+".abstract"
		#fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),cyclic_adj_list,fn+".decomp.cyclic.",widths=[6],vsdeg=False,nByi=data["nByi"],directed=True)
		#fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),div_adj_list,fn+".decomp.acyclic.",widths=[6],vsdeg=False,nByi=data["nByi"],directed=True)
		#fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),data["adj"],fn+".decomp.acyclic.over.all.",widths=[6],vsdeg=False,nByi=data["nByi"],adj_list2=div_adj_list,directed=True)
		#fiedler.doPlots(numpy.array(data["f1"]),-1*numpy.array(rank),numpy.array(data["d"]),cyclic_adj_list,fn+".decomp.harmonic.v.grad.",widths=[6],heights=[2],vsdeg=False,nByi=data["nByi"],directed=True)
		#fiedler.doPlots(numpy.array(data["f1"]),-1*numpy.array(rank),numpy.array(data["d"]),skew,fn+".decomp.skew.v.grad.",widths=[6],heights=[2],vsdeg=False,nByi=data["nByi"],directed=True)
		#fiedler.doPlots(numpy.array(data["f1"]),-1*numpy.array(rank),numpy.array(data["d"]),data["adj"],fn+".decomp.acyclic.over.all.v.grad.",widths=[6],heights=[2],vsdeg=False,nByi=data["nByi"],adj_list2=div_adj_list,directed=True)
		fiedler.doPlots(numpy.array(data["f1"]),-1*numpy.array(rank),numpy.array(data["d"]),data["adj"],fn+".all.v.grad.",widths=[16],heights=[4],vsdeg=False,nByi=data["nByi"],directed=True)
		#fiedler.doPlots(numpy.array(data["f1"]),-1*numpy.array(rank),numpy.array(data["d"]),data["adj"],fn+".all.enriched.0002",widths=[6],heights=[2],vsdeg=False,nByi=data["nByi"],directed=True,enrichdb="../GraphSpec/homo-sapiens-9606-gene-symbol.gmt",clust_x=.0002,clust_xy=False,dorank=False)

def main():
	fn=sys.argv[1]
	
	plotjson(fn)
	


if __name__ == '__main__':
	main()