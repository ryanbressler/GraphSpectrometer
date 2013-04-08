#!/usr/bin/env python

# Dick Kreisberg March 2013

# Take a ruleset of the types of features to "keep"
# Identify the list of features that match the ruleset from the specified feature matrix
# extract the headers and feature rows from the feature matrix
# output the new feature matrix

import sys

#   rule is tab delimited set of fields.  1st column indicates whether the rule allows or disallows matching feature
#   2nd-? columns are used for matching current feature_id fields
#   '*' or whitespace allows any value
#   '' or 'A' or 'ALLOW' creates an allow rule
#   'D' or 'DISALLOW' creates a disallow rule

def read_ruleset(filename):
    disallowRules = []
    allowRules = []
    comments = ['#','%','//']

    f = open(filename,'r')
    header = f.readline()

    for rule in f:
        fields = rule.strip().split("\t")
        allow = fields[0].strip().upper()
        #detect comment and move to next line
        if ( any(allow[0] == substring for substring in comments) ):
            continue
        if ( len(allow) < 1 ):
            continue
        if ( allow.upper() == 'A' or allow.upper() =='ALLOW' or len(allow) < 1 ):
            if ( len(fields) > 1 ):
                allowRules.append(fields[1:])
            else:
                allowRules.append(['*'])
        elif ( allow.upper() =='D' or allow.upper =='DISALLOW' ):
            disallowRules.append(fields[1:])

    f.close()

    return (allowRules, disallowRules)

def extract_matches( input_fm, output_fm, allow_rules, disallow_rules ):
    output = []
    print "Allow:"
    print allow_rules
    print "Disallow:"
    print disallow_rules
    try:
        fm = open(input_fm,'r')
        extracted_fm = open(output_fm,'w')

        #get header!
        line = fm.readline()
        extracted_fm.write(line)
        
        for line in fm:
            if ( matches(line, allow_rules) and not matches(line, disallow_rules) ):
                extracted_fm.write(line)
                
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Error when extracting matches:", sys.exc_info()[0]
    finally:
        fm.close()
        extracted_fm.close()

    return    

# does the feature match at least one rule in the list of rules?
def matches(feature_row, rules):
    feature_id = feature_row.strip()[0:feature_row.index('\t')]
    feature_fields = feature_id.split(':')
    num_features = len(feature_fields)
    passes_any_rule = False
    for rule in rules:
        passes_rule = True
        #if there are more feature fields than rules defined, it is assumed to accept the rest of the fields.
        for index, field in enumerate(rule):
            # if there are more rules than feature fields, there is nothing to check.  so accept the feature
            if (num_features < index + 1 ):
                break
            
            clean_field = field.strip()

            if ( len(clean_field) < 1 or clean_field == "*"):
                continue
            if (feature_fields[index] == clean_field):
                continue
            # the feature absolutely does not match the defined rule
            passes_rule = False
            break
        passes_any_rule = passes_any_rule or passes_rule

    return passes_any_rule

def parse_parameters():
    import argparse
    parser = argparse.ArgumentParser(description = 'Subset Feature Matrix by features according to a ruleset for acceptable features')
    parser.add_argument('--fm', nargs = '?' , required=True,
                            help = 'input Feature Matrix file. e.g. /path/to/data/disease.fm')
    parser.add_argument('--feature_def', nargs = '?', required=True,
                            help = 'input feature ruleset definition file. e.g. /path/to/feature/ruleset.tsv')
    parser.add_argument('--out', nargs = '?', const = 'subset.tsv', default = 'subset.tsv', 
                            help = 'output subset Feature Matrix file. e.g. /path/to/output/subset.fm')
    return parser.parse_args()

def main(): 

    args = parse_parameters()
    # read feature ruleset
    allow_rules, disallow_rules = read_ruleset(args.feature_def)

    #write out all features that match allow_rules and do not match disallow_rules
    extract_matches(args.fm, args.out, allow_rules, disallow_rules)

if __name__ == '__main__':
    main()