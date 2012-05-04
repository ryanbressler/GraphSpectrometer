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
		A = fiedler.adj_mat(data["adj"])
		#scew symetricise 
		A = (A.T - A)/2
		#TODO subtract out curl

		adj2=fiedler.adj_list(A)
		fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),data["adj"],fn,widths=[64],vsdeg=False,nByi=data["nByi"],adj_list2=adj2)

def main():
	fn=sys.argv[1]
	
	plotjson(fn)
	


if __name__ == '__main__':
	main()