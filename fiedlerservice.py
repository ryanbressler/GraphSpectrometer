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
	accepts a post body of the form
	node1\tnode2\n
	...
	"""

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