import sys
import json
import math
import fiedler


def parserow(line):
    #DOES NOT RETURN CORRECT VALUES FOR VALUES WITH COMMAS IN THEM
    clauses=[]
    insidequotes=[]
    for term in line.strip().split(","):
        quotes = term.count('"')
        if quotes == 1 or len(insidequotes)>0:
            insidequotes.append(term)
        else:
            clauses.append(term)
        if quotes == 1 and len(insidequotes) > 1:
            clauses.append(",".join(insidequotes))
            insidequotes=[]

    return dict([[c.strip().strip('"').strip() for c in b] for b in [a.split("=") for a in clauses] if len(b) == 2])
    #return dict([[c.strip("\"") for c in b] for b in [a.split("=") for a in line.split(",")] if len(b) == 2])


def parseRfPredict(fo, cutoff):
    adj_hash = {}
    spliter_by_feature ={}
    predicted = "UNKNOWN"
    ntrees = 0
    treeid = 0
    parents = {"": predicted}
    for i, line in enumerate(fo):
        try:
            if line[:6] == "FOREST":
                vhash = parserow(line)
                predicted = vhash["TARGET"]
            elif line[:4] == "TREE":
                ntrees += 1
                treeid = parserow(line)["TREE"]
                parents = {"": predicted}
            elif line[:4] == "NODE":
                vhash = parserow(line)
                if "SPLITTER" in vhash:
                    source = vhash["SPLITTER"]
                    node = vhash["NODE"]
                    parents[node] = source
                    target = parents[node[:-1]]
                    vhash["parents"] = [parents[node[:-n]] for n in range(1, len(node))]
                    vhash["treeid"] = treeid
                    if not source in spliter_by_feature:
                        spliter_by_feature[source] = []
                    spliter_by_feature[source].append(vhash)
                    if not source in adj_hash:
                        adj_hash[source] = {}
                    if not target in adj_hash[source]:
                        adj_hash[source][target] = 1.0
                    else:
                        adj_hash[source][target] += 1.0  
        except:
            print "Error parsing line %s: %s\nparents:%s" % (i, line, parents)
            raise

    out = []
    intidsbyname = {}
    namesbyintid = []

    incintid = 0

    for source in adj_hash:
        for target in adj_hash[source]:
            if adj_hash[source][target] > cutoff:
                for strid in [source, target]:
                    if not strid in intidsbyname:
                        intidsbyname[strid] = incintid
                        namesbyintid.append(strid)
                        incintid += 1
                row = [intidsbyname[source], intidsbyname[target], float(adj_hash[source][target])]
    
                out.append(row)

    return (out, intidsbyname, namesbyintid, spliter_by_feature)


def main():
    fn = sys.argv[1]
    fo = open(fn)
    cutoff = 1.0
    if len(sys.argv) > 2:
        cutoff = float(sys.argv[2])
        fn += "cutoff"+str(cutoff)
    
    (adj_list, iByn, nByi, spliter_by_feature) = parseRfPredict(fo, cutoff)
    fo.close()
    print "adj_list", numpy.array(adj_list).shape
    fied = fiedler.fiedler(adj_list, fn=fn, plot=False, n_fied=2)
    fied["adj"] = adj_list
    fied["iByn"] = iByn
    fied["nByi"] = nByi
    fied["sByf"] = spliter_by_feature
    fo = open(fn + ".json", "w")
    json.dump(fied, fo, indent=2)
    fo.close()

if __name__ == '__main__':
    main()
