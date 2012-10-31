import os
import sys
import json

import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from scipy import sparse
import matplotlib.gridspec as gridspec
import scipy.spatial.distance as distance

import fiedler

def filename_parse(fn, filter_min=.001,col=2,filter_col=2):
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

    out = fiedler.file_parse(fo, node2=1, filter_col=filter_col, filter_min=filter_min, val_col=col)
    
    fo.close()
    return out

def MDS(adj_list):
    (A,adj,Npts) = fiedler.adj_mat(adj_list)
    D = A.todense()

    #converting to distance...may not work for importance scores
    D = np.sqrt(1-np.abs(D))

    #from Ryan Tasseff's cmdsAnalysis
    [n,m] = D.shape
    eps = 1E-21
    if n!=m:
        raise ValueError('Wrong size matrix')

    # Construct an n x n centering matrix
    # The form is P = I - (1/n) U where U is a matrix of all ones
    P = np.eye(n) - (1/float(n) * np.ones((n,n)))
    # center the data 
    B = np.dot(np.dot(P,-.5*D**2),P)
    # if len(w)>0:
    #     W = np.diag(np.sqrt(w))
    #     B = np.dot(np.dot(W,B),W)
        
    # Calculate the eigenvalues/vectors
    [E, V] = linalg.eig((B+B.T)/2) # may help with round off error??
    E = np.real(E) # these come out as complex but imaginary part should b ~eps
    V = np.real(V) # same as above
    # if len(w)>0:
    #     W = np.diag(1/np.sqrt(w))
    #     V = np.dot(W,V)
    # sort that mo fo
    ind = np.argsort(E)[::-1]
    E = E[ind]
    V = V[:,ind]
    # lets now create our return matrix 
    if np.sum(E>eps)==0:
        Y = 0
    else:
        Y = V[:,E>eps]*np.sqrt(E[E>eps])
    return {"m1":list(Y[:,0]), "m2":list(Y[:,1])}
    #return(Y,E)

def main():
    fn = sys.argv[1]
    filter_min = ""
    
    filter_min = float(sys.argv[2])
    
    col = int(sys.argv[3])
    filter_col = col
    if len(sys.argv)>4:
        filter_col=int(sys.argv[4])
    print "Parseing %s min %s val_col %s filter_col %s"%(os.path.abspath(fn),filter_min,col,filter_col)


    (adj_list, iByn, nByi) = filename_parse(fn, filter_min, col, filter_col)

    fied = MDS(adj_list)
    fied["adj"] = adj_list
    fied["iByn"] = iByn
    fied["nByi"] = nByi

    outfn=os.path.basename(fn) +".cutoff."+ str(filter_min) + ".json"
    fo = open(outfn, "w")
    print "Outputing MDS results for %s to %s"%(os.path.abspath(fn),os.path.abspath(outfn))
    json.dump(fied, fo)
    fo.close()

if __name__ == '__main__':
    main()