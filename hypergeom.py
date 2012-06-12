import numpy as numpy
from scipy.stats import hypergeom

def loadList(filename):
	fo= open(sys.argv[1])
	data = np.array(fo.read().rstrip().split())
	fo.close()
	return data

def enrich(genes,background,dbfilename,verbose=False):
	ntrys = len(genes)
	total= len(background)
	gmtDB = open(sys.argv[3]):
	names =[]
	links =[]
	probs =[]
	for line in gmtDB:
		vs=line.rstrip().split()
		setgenes=np.array(vs[2:])
		nfound = np.sum(np.in1d(genes,setgenes))
		npresent = np.sum(np.in1d(setgenes,background))
		prob = hypergeom.sf(nfound,total,npresent,ntrys)
		names.append(vs[0])
		links.append(vs[1])
		probs.append(prob)
		print "\t".join([*vs[:2],str(prob))
	

def main():
	genes = loadList(sys.argv[1])
	background = loadList(sys.argv[2])
	enrich(genes,background,sys.argv[3])

if __name__ == '__main__':
	main()