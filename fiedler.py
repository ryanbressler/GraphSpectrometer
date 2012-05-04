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

Can also be used on rf-ace output files provided the file has a ".out" exstension.

Or with x args as a thread pool to plot many sif files:
ls *.sif | xargs --max-procs=8 -I FILE  python fiedler.py FILE


By default generates a number of pngs of diffrent sorts of plots and a .json file containing: 

{"f1": the first fiedler vector,
"f2": (if caclulated) the second fideler vector
"d": the node degrees,
"r1": the rank of each node in the first fiedler vector
"r2": the rank of each node in the second fiedler vector
"iByn": the index of the nodes by the string used to represent them in the input file
"nByi": the string used to represent nodes in the input file by their index in the graph
"adj": the adjascancy list}

Author/Contact:Ryan Bressler, ryan.bressler@systemsbiology.org

"""



import sys
import json
import math

from scipy.sparse import coo_matrix

import numpy
import scipy
from scipy.sparse.linalg import lobpcg

from pyamg import smoothed_aggregation_solver







def file_parse(fo,node1=0,node2=2,filter_col=-1,filter_min=.5,val_col=-1):
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
			if filter_col!=-1:
				if float(vs[filter_col])<filter_min:
					continue
			for strid in [vs[node1],vs[node2]]:
				if not strid in intidsbyname:
					intidsbyname[strid]=incintid
					namesbyintid.append(strid)
					incintid = incintid+1 
			row =[intidsbyname[vs[node1]],intidsbyname[vs[node2]]]

			if val_col!=-1:
				row.append(float(vs[val_col]))

			
			out.append(row)
		
	fo.close()
	return (out,intidsbyname,namesbyintid)

def adj_mat(adj_list):
	"""get the graph laplacian (in coo_matrix sparse matrix form) of an 
	adjancy list.0
	
	Takes:

	An Nx2 nested list of ints of the form:
	[[node1,node2],
	...]
	or an Nx3 list in the form:
	[[node1,node2,value],
	...]
	Representing the adjascancy list.

	Returns
	The adjasancy matrix in coo_matrix format.
	"""
	adj=numpy.array(adj_list)
	Npts = numpy.max(adj)+1
	data = numpy.ones(adj.shape[0],dtype=float)
	if adj.shape[1]>2:
		data=-1*adj[:,2]
	A = coo_matrix((data,(adj[:,0],adj[:,1])), shape=(Npts,Npts))
	return A

def adj_list(adj_mat,includeValue=True):
	am=adj_mat.tocoo()
	rv=numpy.column_stack((am.row,am.col,am.data)).tolist()
	for row in rv:
		row[0]=int(row[0])
		row[1]=int(row[1])
	return rv


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
	A = adj_mat(adj_list)
	A = (A.T + A)/2
	A=A.tocsr()
	if adj_list.shape[1]==2:
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
		doPlots(evec[:,1],evec[:,2],A.diagonal(),adj_list,fn)
		
		
	out = {"f1":list(evec[:,1]),"d":list(A.diagonal()),"r1":[int(i) for i in list(numpy.argsort(numpy.argsort(evec[:,1])))]}
	if n_fied > 1:
		out["f2"]=list(evec[:,2])
		out["r2"]=[int(i) for i in list(numpy.argsort(numpy.argsort(evec[:,2])))]
	return out
	

def doPlotingImport():
	global mpath,mpatches,plt
	import matplotlib.path as mpath
	import matplotlib.patches as mpatches
	import matplotlib.pyplot as plt


#Plots are not optimized ...ie they end up sorting the same thing multiple times
def doPlots(f1,f2,degrees,adj_list,fn,widths=[16],vsdeg=True,nByi=False,adj_list2=False):
	doPlotingImport()
	# output first
	if vsdeg:
		plotFiedvsDeg(f1,degrees,fn)

	#if n_fied>1:
	for width in widths:
		#output fied vs fied:
		plotFiedvsFied(f1,f2,fn,adj_list=adj_list,adj_list2=adj_list2,width=width,nByi=nByi)

	#output second
	if vsdeg:
		plotFiedvsDeg(f2,degrees,fn+".second")

def plotEdges(x,y,ax,adj_list,color="green"):
	#codes=[]
	#points=[]
	for edge in adj_list:
		#points[len(points):]=[(x[edge[0]],y[edge[0]]),(x[edge[1]],y[edge[1]])]
		points=[(x[edge[0]],y[edge[0]]),(x[edge[1]],y[edge[1]])]
		#codes[len(codes):]=[mpath.Path.MOVETO,mpath.Path.LINETO]
		codes=[mpath.Path.MOVETO,mpath.Path.LINETO]
		alpha=.5
		if len(edge)>2 and float(edge[2])>0:
			alpha=math.sqrt(float(edge[2]))


		patch = mpatches.PathPatch(mpath.Path(points,codes), edgecolor=color, lw=.3,alpha=alpha)
		ax.add_patch(patch)

def PlotEdgeVvsEdgeV(adj1,adj2,nByi1,nByi2,fn,width=16):
	doPlotingImport()
	edgevs = {}
	nedges = 0
	nByis=[nByi1,nByi2]
	for i,adj in enumerate([adj1,adj2]):
		for edge in adj:
			[e0,e1,v]=edge
			e0=nByis[i][e0]
			e1=nByis[i][e1]
			if not e0 in edgevs:
				edgevs[e0]={}
			if not e1 in edgevs[e0]:
				edgevs[e0][e1]={}
				nedges+=1
			edgevs[e0][e1][i]=float(v)
	x = numpy.zeros((nedges,),dtype=float)
	y = numpy.zeros((nedges,),dtype=float)
	i = 0
	for n0 in edgevs:
		for n1 in edgevs[n0]:
			e = edgevs[n0][n1]
			if 0 in e:
				x[i]=e[0]
			if 1 in e:
				y[i]=e[1]
			i=i+1

	F = plt.figure()
	ax = F.add_subplot(111)
	
	ax.scatter(x, y,zorder=2)
	i = 0
	for n0 in edgevs:
		for n1 in edgevs[n0]:
			plt.annotate(	
		        "->".join([":".join(n.split(":")[1:3]) for n in [n0,n1]]),
		        xy = (x[i], y[i]), xytext = (-0, 0),
		        textcoords = 'offset points', ha = 'right', va = 'bottom',size=6,alpha=.3)
			i+=1

	ax.grid(True)
	F.set_size_inches( (width,width) )
	F.savefig(fn+".EdgeVvsEdgeV.width%s.png"%(width),bbox_inches='tight')
	F.clear()





def plotFiedvsFied(fied1,fied2,fn,adj_list=False,adj_list2=False,width=16,nByi=False):
	""" make scatter plots and rank v rank plots and write to files.

	Takes
	fied1: the fiedler vector to use as the x axis
	fied2: the fiedler vector to use as the y axis
	fn: the filename to prepend"""
	doPlotingImport()
	F = plt.figure()
	ax = F.add_subplot(111)
	
	ax.scatter(fied1, fied2,zorder=2)
	if not adj_list==False:
		plotEdges(fied1,fied2,ax,adj_list)
	if not adj_list2==False:
		plotEdges(fied1,fied2,ax,adj_list2,color="red")
	if not nByi==False and width>32:
		labelPoints(plt,fied1,fied2,nByi=nByi)
	ax.grid(True)
	F.set_size_inches( (width,width) )
	F.savefig(fn+".fied1vfied2.width%s.png"%(width),bbox_inches='tight')
	F.clear()

	F = plt.figure()
	ax = F.add_subplot(111)
	
	sortx=numpy.argsort(numpy.argsort(fied1))
	sorty=numpy.argsort(numpy.argsort(fied2))
	
	ax.scatter(sortx,sorty,zorder=2)
	if not adj_list==False:
		plotEdges(sortx,sorty,ax,adj_list)
	if not adj_list2==False:
		plotEdges(sortx,sorty,ax,adj_list2,color="red")

	if not nByi==False and width>32:
		labelPoints(plt,sortx,sorty,nByi=nByi)
			

	ax.grid(True)
	ax.set_xmargin(.01)
	ax.set_ymargin(.01)

	
	F.set_size_inches( (width,width) )
	F.savefig(fn+"fied1rank.v.fied2rank.width%s.png"%(width),bbox_inches='tight')
	F.clear()

def labelPoints(plt,x,y,nByi):
	for i,xi in enumerate(x):
		plt.annotate(
	        ":".join(nByi[i].split(":")[1:3]), 
	        xy = (xi, y[i]), xytext = (-1, 1),
	        textcoords = 'offset points', ha = 'right', va = 'bottom',size=6,alpha=.4)


def plotFiedvsDeg(fied, degree,fn):
	""" make fied vs degree and fiedler rank vs degree plots and write to files.

	Takes
	fied: the fiedler vector to use as the x axis
	degree: the degree of the nodes
	fn: the filename to prepend"""
	F = plt.figure()
	ax = F.add_subplot(111)
	ax.scatter(fied, numpy.log2(degree))
	ax.grid(True)

	F.set_size_inches( (64,8) )
	F.savefig(fn+".fiedler.vs.log2.degree.png")
	F.clear()

	F = plt.figure()
	ax = F.add_subplot(111)

	order = numpy.argsort(fied)
	ax.scatter(numpy.arange(0,fied.size), numpy.log2(degree[order]))
	ax.grid(True)

	F.set_size_inches( (64,8) )
	F.savefig(fn+".fiedler.ranks.vs.log2.degree.png")
	F.clear()

	
def filename_parse(fn,filter_min=.001):
	"""Wraps file_parse and infers paramaters based on extensions.

	Takes:
	filename.

	".out" files will be treated as rf-ace output and filtered by imortance

	all other files will be treated as sif files.

	returns:
	The same tuple as filename_parse
	"""

	fo = open(fn)
	out =()
	if fn[-4:]==".out":
		out =file_parse(fo,node2=1,filter_col=3,filter_min=filter_min,val_col=3)
	else:
		out= file_parse(fo)
	fo.close()
	return out

def main():
	
	fn = sys.argv[1]
	filter_min=""
	if len(sys.argv)>2:
		filter_min=float(sys.argv[2])
	(adj_list,iByn,nByi)=filename_parse(fn,filter_min)
	fied=fiedler(adj_list,fn=fn+str(filter_min),plot=False,n_fied=2)
	fied["adj"]=adj_list
	fied["iByn"]=iByn
	fied["nByi"]=nByi
	fo = open(fn+str(filter_min)+".continuous.json","w")
	json.dump(fied,fo)
	fo.close()


if __name__ == '__main__':
	main()





