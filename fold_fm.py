#!/usr/bin/env python

# Dick Kreisberg March 2013

# Take definition of folds (subsets of samples)
# Map the ids used in the fold list to the actual ids in the feature matrix
# split the Feature Matrix into training/testing subsets
# output each set.

from pandas import *

    # Training fold: value = 0
    # Testing fold: value = 1
def get_rows_by_value(frame, repetition_number, fold_number, value):
    return frame[frame['Repeat' + repetition_number + 'Fold' + fold_number] == value]

def get_column_ids(frame):
    return frame['SampleIDs']

def read_file_to_frame(filename):
    return read_table(filename, sep = '\t', na_values = '', header=0)

def map_sample_indexes(ids, possible_matches):
    index_list = []
    for id in ids:
        for i, d in enumerate(possible_matches):
            if (d.startswith(id)):
                index_list.append(i)
    return index_list

def cut_feature_matrix(index_list, fm_filename, output_filename):
    import os
    # cut uses a 1-based index for columns
    # cast integers to strings for commandline
    os.system('cut -f '+ ",".join(str(i+1) for i in index_list) + ' ' + fm_filename + ' > ' + output_filename)

def parse_parameters():
    import argparse
    parser = argparse.ArgumentParser(description = 'Subset Feature Matrix by samples according to fold definition and specified fold/repetition')
    parser.add_argument('--fm', nargs = '?' , required=True,
                            help = 'input Feature Matrix file. e.g. /path/to/data/disease.fm')
    parser.add_argument('--fold_list', nargs = '?', required=True,
                            help = 'input fold definition file. e.g. /path/to/folds/folds.tsv')
    parser.add_argument('--fold_number', nargs = '?', const = 0, default = 1, 
                            help = 'integer defining the fold number.  1-based index. (defaults to 1)')
    parser.add_argument('--repetition_number', nargs = '?', const = 0, default = 1,
                            help = 'integer defining the repetition number.  1-based index. (defaults to 1)')
    parser.add_argument('--train', nargs = '?', const = 'train.tsv', default = 'train.tsv', 
                            help = 'output training fold Feature Matrix file. e.g. /path/to/output/training.fm')
    parser.add_argument('--test', nargs = '?', const = 'test.tsv', default = 'test.tsv',
                            help = 'output testing fold Feature Matrix file. e.g. /path/to/output/testing.fm')
    return parser.parse_args()


def main(): 

    args = parse_parameters()
    # read fold list into data frame
    fold_frame = read_file_to_frame(args.fold_list)

    #get all rows that match the training fold value
    training_frame = get_rows_by_value(fold_frame, args.repetition_number, args.fold_number, 0)

    #get all rows that match the testing fold value
    testing_frame = get_rows_by_value(fold_frame, args.repetition_number, args.fold_number, 1)

    # grab the string identifier for the sample
    training_ids = get_column_ids(training_frame)
    testing_ids = get_column_ids(testing_frame)

    # read feature matrix into data frame
    fm_frame = read_file_to_frame(args.fm)

    # map the fold data to the feature matrix id's
    mapped_training_ids = map_sample_indexes(training_ids, fm_frame.columns)
    mapped_testing_ids = map_sample_indexes(testing_ids, fm_frame.columns)

    #keep the feature id column at the front!
    mapped_training_ids.insert(0,0)
    mapped_testing_ids.insert(0,0)

    #send the cut command to the OS (Linux or MacOS)
    cut_feature_matrix(mapped_training_ids, args.fm, args.train)
    cut_feature_matrix(mapped_testing_ids, args.fm, args.test)

if __name__ == '__main__':
    main()