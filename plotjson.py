"""
plotjson.py

Script to make plots from json files calculated by fiedler.py

usage:

python plotjson.python fiedler.out.json

or often:
ls *.json | xargs --max-procs=10 -I FILE  python plotjson.py FILE

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
		fiedler.doPlots(numpy.array(data["f1"]),numpy.array(data["f2"]),numpy.array(data["d"]),data["adj"],fn,widths=[16],vsdeg=False,nByi=data["nByi"])

def main():
	fn=sys.argv[1]
	
	plotjson(fn)
	


if __name__ == '__main__':
	main()