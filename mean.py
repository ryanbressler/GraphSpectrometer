#!/usr/bin/env python
import sys

def main():
	count = {}
	error = {}
	for line in sys.stdin:
		vs = line.rstrip().split()
		if True!=(vs[0] in count):
			count[vs[0]]=0
			error[vs[0]]=0.0
		count[vs[0]]+=1
		error[vs[0]]+=float(vs[1])
	for name,c in count:
		print "%s\t%s"%(name,string(error[name]/c))

if __name__ == '__main__':
	main()
