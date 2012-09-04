import sys
import json
import fiedler


def parseRfPredict(fo):
    adj_hash = {}
    predicted = "UNKNOWN"
    for line in fo:
        parents = {"": predicted}
        terms = [v.split("=") for v in line.rstrip().split(",")]
        if terms[0][0] == "FOREST":
            predicted = terms[0][1]
        elif terms[0][0] == "TREE":
            parents = {"": predicted}
        elif terms[0][0] == "NODE":
            vhash = dict(terms)
            if "SPLITTER" in vhash:
                source = vhash["SPLITTER"]
                node = vhash["NODE"]
                parents[node] = source
                target = parents[node[:-1]]
                if not source in adj_hash:
                    adj_hash[source] = {}
                if not target in adj_hash[source]:
                    adj_hash[source][target] = 1
                else:
                    adj_hash[source][target] += 1

    out = []
    intidsbyname = {}
    namesbyintid = []

    incintid = 0

    for source in adj_hash:
        for target in adj_hash["source"]:
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
