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


def fiedler(adj_list,fn):
	"""calculate the first fiedler vector of a graph adjascancy list 
	given as a two dimensional arrya of ints of the form:
	[[node1,node2],
	...]"""

	A = graph_laplacian(adj_list)

	# construct preconditioner
	ml = smoothed_aggregation_solver(A, coarse_solver='pinv2',max_coarse=10)
	M = ml.aspreconditioner()

	# solve for lowest two modes: constant vector and Fiedler vector
	X = scipy.rand(A.shape[0], 2) 
	(eval,evec,res) = lobpcg(A, X, M=None, tol=1e-12, largest=False, \
	        verbosityLevel=0, retResidualNormsHistory=True)

	fied= evec[:,1]
	output(fied,A.diagonal(),fn)
	return fied

def output(fied, degree,fn):
	pylab.scatter(fied, numpy.log2(degree))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+"fiedler.png")
	F.clear()

	order = numpy.argsort(fied)
	pylab.scatter(numpy.arange(0,order.size), numpy.log2(degree[order]))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+"fiedler.sorted.png")
	
	print json.dumps({"f":list(fied),"d":list(degree),"o":[int(i) for i in list(order)]})

def main():
	fn = sys.argv[1]
	adj_list=sif_parse(fn)
	fied = fiedler(adj_list,fn)



if __name__ == '__main__':
	main()





