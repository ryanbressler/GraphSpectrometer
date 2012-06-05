"""
plotGMM.py

Script to make plots from json files calculated by fiedler.py not including edges but includeing clusters derived from GMM

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
	
	#fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),data["adj"],fn,widths=[64],vsdeg=False,nByi=data["nByi"])
	fiedler.plotFiedvsFied(numpy.array(data["f1"]),numpy.array(data["f2"]),fn+".dbscan.",data["adj"],width=32,nByi=data["nByi"],dbscan_eps=.01,dbscan_rank_eps=32)

def main():
	fn=sys.argv[1]
	
	plotjson(fn)
	


if __name__ == '__main__':
	main()