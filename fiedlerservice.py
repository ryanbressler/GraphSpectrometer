#!/usr/bin/env python
"""
a simple cgi webservice that accepts a sif like post body and returns

json of the form
[{"f1": -0.011036646594476215, "f2": -0.025580268321166274, "r1": 863, "r2": 216, "d": 1.0, "name": "79682"},
...]
"""

import sys
import json
import fiedler

def RequestHandler(info,outfo):
	"""
	Parse input,do caclulation, transform into proper format and dump json.

	info: a file like object containing a sif like file
	outfo: a file like object to write json to
	"""

	#Change 2 to 1 below to accept 2 column files.
	#Could also parse json of the form [["node1","node2"],...] with something like
	#(adj_list,iByn,nByi)=fiedler.file_parse(["%s\t%s"%(e[0],e[1]) for e in json.load(info)],0,2)
	(adj_list,iByn,nByi)=fiedler.file_parse(info,0,2)
	fied=fiedler.fiedler(adj_list,plot=False,n_fied=2)
	out = fied["f1"][:]
	for i,name in enumerate(nByi):
		out[i]={"name":name}
		for key in fied:
			if not key in ["iByn", "nByi"]:
				out[i][key]=fied[key][i]
	json.dump(out,outfo)

def main():
	RequestHandler(sys.stdin,sys.stdout)

if __name__ == '__main__':
	main()