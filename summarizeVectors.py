#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json

import numpy as np
from scipy import stats


# take a list of numerical values that were used to split a feature.
# generate a histogram of the splits

# fn is the json file that is being appended to
# fm is the feature matrix TSV file
# splits is the file holding the list of splits for each feature

def featureSplitValues(fn, fm, splits):

    fo = open(fn)
    data = json.load(fo)
    fo.close()

    fo = open(fm)

    # colheaders=fo.next().rstrip().split("\t")[1:]
    # skip the first line

    fo.next()
    rowheaders = []

    # read in the feature names

    for line in fo:
        rowheaders.append(line.rstrip().split('\t')[0])

    # read in the splits
    # each line is feature_id_integer split1 split2 ... (varying length)

    split_entries = {}
    fo = open(splits)
    for line in fo:
        vs = [float(v) for v in line.rstrip().split('\t')]
        split_entries[int(vs[0])] = np.array(vs[1:])

    fo.close()

    matrix = []
    split_list = []

    for f_index in split_entries:
        split_list = split_entries[f_index]
        # don't worry about very few splits

        (bins, low, binsize,extra) = stats.histogram(split_list)

        bin_list = []
        significant = False

        for (index, count) in enumerate(bins):
            if count > 50:
                significant = True
            bin_list.append({ "position" : low + (binsize * index),
                            "count" : count
                            })
        if significant == True:
            feature_name = rowheaders[f_index]
            split_line = [feature_name]
            split_line.append(bin_list)
            matrix.append(split_line)

    return matrix


def main():
    fn = sys.argv[1]
    fm = sys.argv[2]
    splits = sys.argv[3]
    splitmatrix = sys.argv[4]
    print 'Generating splits matrix using  %s %s %s %s' \
        % (os.path.abspath(fn), os.path.abspath(fm), splits,
           splitmatrix)
    matrix = featureSplitValues(fn, fm, splits)

    print 'Outputing splitmatrix to %s from %s and %s' % (splitmatrix,
            fm, splits)
    fo = open(splitmatrix, 'w')
    for row in matrix:
        fo.write('%s\n' % '\t'.join([str(e) for e in row]))
    fo.close()


if __name__ == '__main__':
    main()
