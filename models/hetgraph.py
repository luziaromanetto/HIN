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
    def __init__(self, m = 0, types = None, v=None, e=None, w=None):
        self.m = m
        self.types = types
        self.V = v
        self.E = e
        self.W = w

    def read_database(directory):
    ''' The database have to be organized as follow to be readed:

    '''
