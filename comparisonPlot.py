import sys
import json
import numpy
import fiedler


def main():
	data = []
	for i,fn in enumerate(sys.argv[1:3]):
		fo = open(fn)
		data.append(json.load(fo))
		data[i]["f1"]=numpy.array(data[i]["f1"])
		fo.close()

	d0index = []
	d1index = []
	for feature in data[0]["iByn"]:
		if feature in data[1]["iByn"]:
			d0index.append(data[0]["iByn"][feature])
			d1index.append(data[1]["iByn"][feature])

	d0index=numpy.array(d0index,dtype="int")
	d1index=numpy.array(d1index,dtype="int")
	fiedler.plotFiedvsFied(data[0]["f1"][d0index],data[1]["f1"][d1index],".vs.".join(sys.argv[1:3]))


if __name__ == '__main__':
	main()