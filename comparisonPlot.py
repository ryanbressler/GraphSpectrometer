import sys
import json
import numpy
import fiedler



def main():
	outfn=".vs.".join(sys.argv[1:3])
	data = []
	for i,fn in enumerate(sys.argv[1:3]):
		fo = open(fn)
		data.append(json.load(fo))
		data[i]["f1"]=numpy.array(data[i]["f1"])
		fo.close()
	

	print "Comparing data set with %i nodes with data set with %i nodes."%(len(data[0]["nByi"]),len(data[1]["nByi"]))
	fiedler.PlotEdgeVvsEdgeV(data[0]["adj"],data[1]["adj"],data[0]["nByi"],data[1]["nByi"],outfn,width=64)
	
	d0index = []
	d1index = []
	nByi=[]
	newi=0
	newiByold=[{},{}]
	for feature in data[0]["iByn"]:
		if feature in data[1]["iByn"]:
			d0index.append(data[0]["iByn"][feature])
			d1index.append(data[1]["iByn"][feature])
			nByi.append(feature)
			newiByold[0][data[0]["iByn"][feature]]=newi
			newiByold[1][data[1]["iByn"][feature]]=newi
			newi+=1
	adjs=[[],[]]
	for i,datum in enumerate(data):
		for e in datum["adj"]:
			[e0,e1,v]=e
			if e0 in newiByold[i] and e1 in newiByold[i]:
				e[0]=newiByold[i][e0]
				e[1]=newiByold[i][e1]
				adjs[i].append(e)
			



	d0index=numpy.array(d0index,dtype="int")
	d1index=numpy.array(d1index,dtype="int")
	fiedler.plotFiedvsFied(data[0]["f1"][d0index],data[1]["f1"][d1index],outfn,adj_list=adjs[0],adj_list2=adjs[1],width=64,nByi=nByi)


if __name__ == '__main__':
	main()