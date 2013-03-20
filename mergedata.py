import sys

def main():
	gcols=[]
	data={}
	for ai,fn in enumerate(sys.argv[1:]):
		print "Grabing data from %s"%(fn)
		fo=open(fn)
		cols=[]
		for li,line in enumerate(fo):
			if li == 0:
				cols=line.rstrip().split()
			if ai == 0:
				gcols=cols[1:]
			if li>0:
				vs = line.rstrip().split()
				data[vs[0]]=dict(zip(cols[1:], vs[1:]))
	print ".\t%s"%("\t".join(gcols[1:]))
	for k,v in enumerate(data):
		print "%s\t%s"%(k,(data[k][id] for id in gcols[1:]))


if __name__ == '__main__':
	main()