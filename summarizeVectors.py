import os
import sys
import json

import numpy as np
from scipy import stats

#take a list of numerical values that were used to split a feature. 
#generate a KDE of the splits

#fn is the json file that is being appended to
#fm is the feature matrix TSV file
#splits is the file holding the list of splits for each feature
def featureSplitValues(fn, fm, splits):

	fo=open(fn)
    data=json.load(fo)
    fo.close()

    fo=open(fm)
    #colheaders=fo.next().rstrip().split("\t")[1:]
    #skip the first line
    fo.next()
    rowheaders=[]
    #read in the feature names
    for line in fo:
        rowheaders.append(line.rstrip().split("\t")[0])

    #read in the splits
    #each line is feature_id_integer split1 split2 ... (varying length)
    splits = {}
    fo = open(splits)
    for line in fo:
        vs = [float(v) for v in line.rstrip().split("\t")]
        splits[vs[0]] = np.array(vs[1:])

    fo.close()
    
    matrix = []

    for feature_index, split_list in enumerate(splits):
    	#don't worry about very few splits
    	if split_list.size < 100
    		continue

        (bins, low, binsize) = stats.histogram(split_list)
        feature_name = rowheaders[feature_index]
        split_line =[feature_name]
        split_line.append([low, binsize])
        split_line.append(bins.tolist())
        matrix.append(split_list)

    return matrix