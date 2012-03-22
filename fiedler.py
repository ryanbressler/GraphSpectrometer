"""

python script/module that uses pyamg to calculat and plot fiedler vectors of sif files.

Comand line Usage:
python fiedler.py my.sif

Or with x args as a thread pool to plot many sif files:
ls *.sif | xargs --max-procs=8 -I FILE  python fiedler.py FILE 


"""


import sys
import json

from numpy import kron, ones, zeros, array
from scipy.sparse import coo_matrix

import numpy
import scipy
from scipy.sparse.linalg import lobpcg

import pylab

from pyamg import smoothed_aggregation_solver

from helper import trimesh, graph_laplacian



def sif_parse(filename):
	"""parse a sif file into an adjascancy list of the form:
	[[node1,node2],
	...]
	"""

	fo = open(filename)
	out = []
	intids = {}
	incintid=0
	for line in fo:
		vs = line.rstrip().split()
		if len(vs)>2:
			for strid in [vs[0],vs[2]]:
				if not strid in intids:
					intids[strid]=incintid
					incintid = incintid+1 

			
			out.append([intids[vs[0]],intids[vs[2]]])
		
	fo.close()
	return out


def graph_laplacian(adj_list):
	"""get the graph laplacian (in sparse matrix form) of an 
	adjancy list given as a two dimensional arrya of ints of the form:
	[[node1,node2],
	...]"""
	adj_list=numpy.array(adj_list)
	Npts = numpy.max(adj_list)+1
	data = numpy.ones(adj_list.shape[0],dtype=float)
	A = coo_matrix((data,(adj_list[:,0],adj_list[:,1])), shape=(Npts,Npts)).tocsr()
	A = A.T + A
	A.data = -1*ones((A.nnz,),dtype=float)
	A.setdiag(zeros((Npts,),dtype=float))
	A.setdiag(-1*array(A.sum(axis=1)).ravel())
	return A.tocsr()


def fiedler(adj_list,fn,plot=False,n_fied=1):
	"""calculate the first fiedler vector of a graph adjascancy list 
	given as a two dimensional arrya of ints of the form:
	[[node1,node2],
	...]"""

	A = graph_laplacian(adj_list)

	# construct preconditioner
	ml = smoothed_aggregation_solver(A, coarse_solver='pinv2',max_coarse=10)
	M = ml.aspreconditioner()

	# solve for lowest two modes: constant vector and Fiedler vector
	X = scipy.rand(A.shape[0], n_fied+1)
	(eval,evec,res) = lobpcg(A, X, M=None, tol=1e-12, largest=False, \
	        verbosityLevel=0, retResidualNormsHistory=True)

	fied= evec[:,1]
	if plot:
		# output first
		plotFiedvsDeg(fied,A.diagonal(),fn)

		if n_fied>1:
			#output fied vs fied:
			plotFiedvsFied(evec[:,1],evec[:,2],fn)

			#output second
			plotFiedvsDeg(evec[:,2],A.diagonal(),fn+".second.")
		
		
	
	return {"f":list(fied),"d":list(A.diagonal()),"o":[int(i) for i in list(numpy.argsort(fied))]}
	



def plotFiedvsFied(fied1,fied2,fn):
	pylab.scatter(fied1, fied2)
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (16,16) )
	F.savefig(fn+".fied1vfied2.png")
	F.clear()

	pylab.scatter(numpy.argsort(fied1), numpy.argsort(fied2))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (16,16) )
	F.savefig(fn+".sorted.fied1vfied2.png")
	F.clear()


def plotFiedvsDeg(fied, degree,fn):
	pylab.scatter(fied, numpy.log2(degree))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+".fiedler.png")
	F.clear()

	#WHY DO THESE TWO METHODS BELOW YIELD DIFFRENT RESULTS??? 
	pylab.scatter(numpy.arange(0,fied.size), numpy.log2(degree[numpy.argsort(fied)]))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+".fiedler.sorted.method1.png")
	F.clear()

	pylab.scatter(numpy.argsort(fied), numpy.log2(degree))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+"fiedler.sorted.png")
	F.clear()

	
	

def main():
	fn = sys.argv[1]
	adj_list=sif_parse(fn)
	print fiedler(adj_list,fn,plot=True,n_fied=2)



if __name__ == '__main__':
	main()





