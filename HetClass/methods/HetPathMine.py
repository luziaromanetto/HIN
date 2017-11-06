import numpy as np
import os
import csv

# -------------------------------------------------------------------- #
class HetPathMine:
# ---------------------------------------------------------------- #
# Inicialization and auxiliar methods
# ---------------------------------------------------------------- #  
    def __init__(self, graph = None, t = None, meta_path = [], beta = None, mu = None):
        self.graph = graph
        self.meta_path = meta_path
        self.beta = beta
        self.mu = mu
        self.t = t
        self.R = dict()
        self.W = dict()
        self.f = list()
        self.target = None

    def build_S(self):
        S = dict()
        for k in self.W:
            Wk = self.W[k]

            dk = np.sum(Wk, axis=1)

            dk = 1.0/(dk**.5)

            S[k] = np.dot(np.diag(dk), Wk )
            S[k] = np.dot(S[k] , np.diag(dk))
            #print k
            #print S[k]

        return S

    def initialize(self):
    # ---------------------------------------------------------------- #
    # Metodo para inicializar as variaveis auxiliares para a iteracao do 
    # metodo
    # ---------------------------------------------------------------- #
        t = self.t
        K = self.graph.get_K() # numero de classes
        self.y = dict()

        nt = self.graph.get_n(t)
        ft = np.zeros( (nt,K) )

        for p in range(nt):
            ct = self.graph.get_c(t,p)
            if ct != -1:
                ft[p,ct] = 1
                self.y[ (t,p) ] = np.zeros(K)
                self.y[ (t,p) ][ct] = 1

        self.f = ft
        
        self.build_similarity_matrix()
        self.S = self.build_S()

    def iterate_f(self):
        W = self.W
        m = len(W)
        t = self.t
        nt = self.graph.get_n(t)
        beta = self.beta
        mu = self.mu
        
        S = self.S
        Scom = np.zeros((nt, nt))
        for k in S:
            Scom += beta[k]*S[k]

        f1 = np.dot(Scom,self.f)
        
        for p in range(nt):
            y = self.y.get((t,p), None)
            if y is not None:
                f1[p] -= mu*(self.f[p] - y)

        return f1

    def build_similarity_matrix(self):
        # i : index od the target object type
        # meta_paths : list of list of meta path order, the first and the
        # last elem of each list have to be iqual to i
        
        # TODO: Test condition of iquality
        graph = self.graph
        m = graph.get_m()
        meta_paths = self.meta_path
        t = self.t
        
        for i in range(m):
            for j in range(m):
                Rij = graph.get_relation_matrix(i,j)
                if Rij is not None:
                    self.R[(i,j)] = Rij

        for mp in meta_paths:
            l = len(mp)
            if l<2 or mp[0] != t or mp[l-1]!=t:
                print "Error in meta path ", t, mp
                continue

            n0 = graph.get_n(mp[0])
            W = np.identity(n0)
            for p in range(l-1):
                i,j= mp[p], mp[p+1]
                Rij = self.R[(i,j)]
                if Rij is None:
                    print "Error do not exist relation between types", i, j, mp
                    W = None
                    continue
                W = np.dot(W, Rij)
                W = W /np.max(W)
                #W = W > 0
                #W = W.astype(int)

            if W is not None:
                k = len(self.W)
                self.W[k] = W
        
    # ---------------------------------------------------------------- #
    # Main method
    # ---------------------------------------------------------------- #
    def run(self, max_it = 100):
        k = 0
        t = self.t

        self.initialize()

        f1 = self.f
        
        # Passo 1
        while k < max_it :
            self.f = f1 
            f1 = self.iterate_f()
            k += 1

        self.f = f1
        # Passo 3
        #print f1
        
        ni = self.graph.get_n(t)
        c = [ -1 ]*ni
            
        for p in range(ni):
            c[p] = np.argmax( self.f[p,:] )

        return c
