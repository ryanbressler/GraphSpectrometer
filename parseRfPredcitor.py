import sys
import json
import math
import fiedler


def parserow(line):
    #DOES NOT RETURN CORRECT VALUES FOR VALUES WITH COMMAS IN THEM
    return dict([[c.strip("\"") for c in b] for b in [a.split("=") for a in line.split(",")] if len(b) == 2])


def parseRfPredict(fo):
    adj_hash = {}
    predicted = "UNKNOWN"
    ntrees = 0
    parents = {"": predicted}
    for i, line in enumerate(fo):
        try:
            if line[:6] == "FOREST":
                vhash = parserow(line)
                predicted = vhash["TARGET"]
            elif line[:4] == "TREE":
                ntrees += 1
                parents = {"": predicted}
            elif line[:4] == "NODE":
                vhash = parserow(line)
                if "SPLITTER" in vhash:
                    source = vhash["SPLITTER"]
                    node = vhash["NODE"]
                    parents[node] = source
                    target = parents[node[:-1]]
                    if not source in adj_hash:
                        adj_hash[source] = {}
                    if not target in adj_hash[source]:
                        adj_hash[source][target] = 1.0
                    else:
                        adj_hash[source][target] += 1.0 / len(node)
        except:
            print "Error parsing line %s: %s\nparents:%s" % (i, line, parents)
            raise

    out = []
    intidsbyname = {}
    namesbyintid = []

    incintid = 0

    for source in adj_hash:
        for target in adj_hash[source]:
            if adj_hash[source][target] > 1:
                for strid in [source, target]:
                    if not strid in intidsbyname:
                        intidsbyname[strid] = incintid
                        namesbyintid.append(strid)
                        incintid += 1
                row = [intidsbyname[source], intidsbyname[target], float(adj_hash[source][target])]
    
                out.append(row)

    return (out, intidsbyname, namesbyintid)


def main():
    fn = sys.argv[1]
    fo = open(fn)
    (adj_list, iByn, nByi) = parseRfPredict(fo)
    fo.close()
    fied = fiedler.fiedler(adj_list, fn=fn, plot=False, n_fied=2)
    fied["adj"] = adj_list
    fied["iByn"] = iByn
    fied["nByi"] = nByi
    fo = open(fn + ".json", "w")
    json.dump(fied, fo)
    fo.close()

if __name__ == '__main__':
    main()
