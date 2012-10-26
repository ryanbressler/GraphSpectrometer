import fiedler

def filename_parse(fn, filter_min=.001,col=2):
    """Wraps file_parse and infers paramaters based on extensions.

    Takes:
    filename.

    ".out" files will be treated as rf-ace output and filtered by imortance

    all other files will be treated as sif files.

    returns:
    The same tuple as filename_parse
    """

    fo = open(fn)
    out = ()

    out = fiedler.file_parse(fo, node2=1, filter_col=2, filter_min=filter_min, val_col=col)
    
    fo.close()
    return out

def main():
    fn = sys.argv[1]
    filter_min = ""
    
    filter_min = float(sys.argv[2])
    col = int(sys.argv[3])

    (adj_list, iByn, nByi) = filename_parse(fn, filter_min,col)
    fn = os.path.basename(fn)
    fied = fiedler.fiedler(adj_list, fn=fn + str(filter_min), plot=False, n_fied=2)
    fied["adj"] = adj_list
    fied["iByn"] = iByn
    fied["nByi"] = nByi
    fo = open(fn + str(filter_min) + ".pwpv.json", "w")
    json.dump(fied, fo)
    fo.close()