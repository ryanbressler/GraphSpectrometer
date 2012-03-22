#!/usr/bin/env python
#
# 
#     Copyright (C) 2003-2012 Institute for Systems Biology
#                             Seattle, Washington, USA.
# 
#     This library is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 2.1 of the License, or (at your option) any later version.
# 
#     This library is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
# 
#     You should have received a copy of the GNU Lesser General Public
#     License along with this library; if not, write to the Free Software
#     Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
# 
"""

python script/module that uses pyamg to calculat and plot fiedler vectors of a graph
using pyamg,numpy and scipy.

Input:
A sif file or any three column white space deliminated file with the first and 
third column repesenting node names and each row repesenting an edge.

Comand line Usage:
python fiedler.py my.sif

Or with x args as a thread pool to plot many sif files:
ls *.sif | xargs --max-procs=8 -I FILE  python fiedler.py FILE


By default generates a number of pngs of diffrent sorts of plots and a .json file containing: 

{"f1": the first fiedler vector,
"f2": (if caclulated) the second fideler vector
"d": the node degrees,
"r1": the rank of each node in the first fiedler vector
"r2": the rank of each node in the second fiedler vector
"iByn": the index of the nodes by the string used to represent them in the input file
"nByi": the string used to represent nodes in the input file by their index in the graph}

Author/Contact:Ryan Bressler, ryan.bressler@systemsbiology.org

"""



import sys
import json

from scipy.sparse import coo_matrix

import numpy
import scipy
from scipy.sparse.linalg import lobpcg

from pyamg import smoothed_aggregation_solver

import pylab






def file_parse(fo,node1=0,node2=2):
	"""parse a sif like file into an adjascancy list by index in a matrix and node name look up tables. 

	Takes:
	f0: A file like object containing a sif or similar white space deliminated file containing at at least 2
	columns of node names that are legal python dictionary keys deliminated by tabs or spaces.

	node1=0 : the index of the column containing the first node
	node2=2 : the index of the column containing the second node2

	Returns a tuple containing:


	An Nx2 nested list of ints of the form:
	[[node1,node2],
	...]
	Representing the adjascancy list.

	A dictionary containing int ids in the above by the string name in the input file.

	An array of strings containing the name in the input by the int id.
	"""

	
	out = []
	intidsbyname = {}
	namesbyintid = []

	incintid=0
	
	for line in fo:
		vs = line.rstrip().split()
		if len(vs)>node2:
			for strid in [vs[node1],vs[node2]]:
				if not strid in intidsbyname:
					intidsbyname[strid]=incintid
					namesbyintid.append(strid)
					incintid = incintid+1 

			
			out.append([intidsbyname[vs[0]],intidsbyname[vs[2]]])
		
	fo.close()
	return (out,intidsbyname,namesbyintid)


def graph_laplacian(adj_list):
	"""get the graph laplacian (in coo_matrix sparse matrix form) of an 
	adjancy list.0
	
	Takes:

	An Nx2 nested list of ints of the form:
	[[node1,node2],
	...]
	Representing the adjascancy list.

	Returns
	The graph laplaciian in coo_matrix format.
	"""
	adj_list=numpy.array(adj_list)
	Npts = numpy.max(adj_list)+1
	data = numpy.ones(adj_list.shape[0],dtype=float)
	A = coo_matrix((data,(adj_list[:,0],adj_list[:,1])), shape=(Npts,Npts)).tocsr()
	A = A.T + A
	A.data = -1*numpy.ones((A.nnz,),dtype=float)
	A.setdiag(numpy.zeros((Npts,),dtype=float))
	A.setdiag(-1*numpy.array(A.sum(axis=1)).ravel())
	return A.tocsr()


def fiedler(adj_list,plot=False,fn="FiedlerPlots",n_fied=2):
	"""calculate the first fiedler vector of a graph adjascancy list and optionally write associated plots to file.

	Takes:
	adj_list:
	An Nx2 nested list of ints of the form:
	[[node1,node2],
	...]
	Representing the adjascancy list.

	plot=False: make plots or not.
	fn="FiedlerPlots": filename to prepend to the plot png file names
	n_fied=2: the number of fiedler vectors to calculate (values above 2 will not be output)

	Returns a Dictionary of the form:



	{"f1": the first fiedler vector,
	"f2": (if caclulated) the second fideler vector
	"d": the node degrees,
	"r1": the rank of each node in the first fiedler vector
	"r2": the rank of each node in the second fiedler vector}


	"""

	A = graph_laplacian(adj_list)

	# construct preconditioner
	ml = smoothed_aggregation_solver(A, coarse_solver='pinv2',max_coarse=10)
	M = ml.aspreconditioner()

	# solve for lowest two modes: constant vector and Fiedler vector
	X = scipy.rand(A.shape[0], n_fied+1)
	(eval,evec,res) = lobpcg(A, X, M=None, tol=1e-12, largest=False, \
	        verbosityLevel=0, retResidualNormsHistory=True)

	if plot:
		# output first
		plotFiedvsDeg(evec[:,1],A.diagonal(),fn)

		if n_fied>1:
			#output fied vs fied:
			plotFiedvsFied(evec[:,1],evec[:,2],fn)

			#output second
			plotFiedvsDeg(evec[:,2],A.diagonal(),fn+".second")
		
		
	out = {"f1":list(evec[:,1]),"d":list(A.diagonal()),"r1":[int(i) for i in list(numpy.argsort(numpy.argsort(evec[:,1])))]}
	if n_fied > 1:
		out["f2"]=list(evec[:,2])
		out["r2"]=[int(i) for i in list(numpy.argsort(numpy.argsort(evec[:,2])))]
	return out
	


#Plots are not optimized ...ie they end up sorting the same thing multiple times

def plotFiedvsFied(fied1,fied2,fn):
	""" make scatter plots and rank v rank plots and write to files.

	Takes
	fied1: the fiedler vector to use as the x axis
	fied2: the fiedler vector to use as the y axis
	fn: the filename to prepend"""

	pylab.scatter(fied1, fied2)
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (16,16) )
	F.savefig(fn+".fied1vfied2.png")
	F.clear()

	pylab.scatter(numpy.argsort(numpy.argsort(fied1)), numpy.argsort(numpy.argsort(fied2)))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (16,16) )
	F.savefig(fn+"fied1rank.v.fied2rank.png")
	F.clear()


def plotFiedvsDeg(fied, degree,fn):
	""" make fied vs degree and fiedler rank vs degree plots and write to files.

	Takes
	fied: the fiedler vector to use as the x axis
	degree: the degree of the nodes
	fn: the filename to prepend"""

	pylab.scatter(fied, numpy.log2(degree))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+".fiedler.vs.log2.degree.png")
	F.clear()

	order = numpy.argsort(fied)
	pylab.scatter(numpy.arange(0,fied.size), numpy.log2(degree[order]))
	pylab.grid(True)
	F = pylab.gcf()
	F.set_size_inches( (64,8) )
	F.savefig(fn+".fiedler.ranks.vs.log2.degree.png")
	F.clear()

	
	

def main():
	
	fn = sys.argv[1]
	fo = open(fn)
	(adj_list,iByn,nByi)=file_parse(fo)
	fo.close()
	fied=fiedler(adj_list,fn=fn,plot=True,n_fied=2)
	fied["iByn"]=iByn
	fied["nByi"]=nByi
	fo = open(fn+".json","w")
	json.dump(fied,fo)
	fo.close()


if __name__ == '__main__':
	main()





