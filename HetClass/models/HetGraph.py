import numpy as np

from os import listdir
from os.path import isfile, join

import csv

class HetGraph(object):
    '''The core class HetGraph

    Parameters
    ----------

    Attributes
    ----------
    m : Number of types in the heterogeneous graph

    types : list of names from the m types of nodes in the graph 

        [ type1, type2, ..., typem]

    V : Dictionary that maps from types to the nodes of each type that 
        is in the graph

        { type1 : [node1, node2, ..., noden1],
          type2 : [node1, node2, ..., noden2],
          ...
          typem : [node1, node2, ..., nodenm] }

    E : Dictionary that maps from a tuple of (type, type) to a bipartide
        directed graph, that is represented as an adjacency list.

        { (type1, type2) : { nodex_type1 : [nodex_type2, nodey_type2],
                            nodey_type1 : [nodew_type2],
                            ... },
         ... }

    W : Not used yet, should be the same structure as E
    '''
    def __init__(self, m = 0, types = list(), v=dict(), e=dict(), w=None):
        self.m = m
        self.types = types
        self.V = v
        self.E = e
        self.W = w
        self.L = dict()
        self.labels = set()

    def read_database(self, path = "../datasets/synt"):
        ''' 
        The database have to be organized as follow to be readed:
        In the input directory should be at least m files .tsv, with the name
        of the types in the graph, the name os the types have to be only
        one low case letters and numbers all together, for exemplos type1.tsv. 
        
        If there is any edge in the gaph, should be more files in the
        directory, this file should have the name of the types of the
        nodes that difine the edges that is described in the file,
        for examplo type1_type2.tsv

        There is an example of the file structure in datasets/synt
        '''

        files = [ f for f in listdir(path) if isfile(join(path, f)) and (".tsv" in f) ]

        node_files = [ f for f in files if len(f[:-4].split("_"))==1 ]
        edge_files = [ f for f in files if len(f[:-4].split("_"))==2 ]
        
        self.m = len(node_files)

        for fname in node_files:
            typei = fname[:-4]
            self.types.append(typei)
            self.V[typei] = dict()
            
            with open(join(path, fname), "rb") as f:
                reader = csv.reader(f, delimiter="\t")
                for line in reader:
                    idi, nodei, labeli = line
                    idi = int(idi)
                    self.V[typei][idi] = nodei
            
                    if labeli != "NULL":
                        self.L[typei] = self.L.get(typei, dict())
                        self.L[typei][idi] = labeli
                        self.labels.add(labeli)

        for fname in edge_files:
        # This method is for non directed graph, so the edges will be 
        # duplicated
            typei, typej = fname[:-4].split("_")

            if typei in self.types and typej in self.types :
                self.E[(typei, typej)] = dict()
                self.E[(typej, typei)] = dict()

                with open(join(path, fname), "rb") as f:
                    reader = csv.reader(f, delimiter="\t")
                    for line in reader:
                        idi, idj, _ = line
                        idi, idj = int(idi), int(idj)
                        
                        # Check if the edge exist before try to add it
                        if idj not in self.E[(typei, typej)].get(idi,[]):
                            self.E[(typei, typej)][idi] = self.E[(typei, typej)].get(idi,[])+[idj] 

                        if idi not in self.E[(typej, typei)].get(idj,[]) :
                            self.E[(typej, typei)][idj] = self.E[(typej, typei)].get(idj,[])+[idi] 

            else:
                print "One of the types dont exist", typei, typej

    def get_relation_matrix(self, typei, typej):
        if self.E.get( (typei, typej) ):
            Eij = self.E[(typei, typej)]
            ni, nj = self.get_n(typei), self.get_n(typej)
            M  = np.zeros( [ni, nj] )

            for nodei in Eij:
                for nodej in Eij[nodei]:
                    M[nodei, nodej] = 1

            return M
        else:
            return None
        
    def get_m(self):
        return self.m

    def get_n(self, i):
        return len(self.V[i])

    def get_K(self):
        return len(self.labels)
    
    def get_labels(self):
        return list(self.labels)

    def get_class(self, i, p):
        if self.L.get(i):
            return self.L[i].get(p)
    
    def get_types(self):
        return list(self.types)
