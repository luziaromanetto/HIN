import numpy as np
import os
import csv

import HetClass
from HetClass.models.HetGraph import HetGraph

# -------------------------------------------------------------------- #
class GNetMine:
    '''
    Attributes
    ----------
    
    '''
# ---------------------------------------------------------------- #
# Inicialization and auxiliar methods
# ---------------------------------------------------------------- #    
    def __init__(self, graph = None, y = None, alpha = 0.1, gamma = 0.2):
        self.graph = graph
        self.y = y
        self.alpha = alpha
        self.gamma = gamma
        self.R = dict()
        self.D = dict()
        self.f = list()
        self.labels = None
        
    def get_relation_matrix(self, i, j):
        return self.R.get((i,j), None)

    def set(self, y = None, alpha = None, gamma = None) :
        if y is not None:
            self.y = y
        
        if alpha is not None:
            self.alpha = alpha

        if gamma is not None:
            self.gamma = gamma

    def build_relation_matrix(self):
        # Do grafo pega as dimensoes dos objetos de tipo i e j
        graph = self.graph
        types = graph.get_types()

        # Para todo par de objetos pergunta a ed do grafo de existe uma 
        # aresta entre eles, se sim atribui o valor de 1 na matriz
        for i in types:
            for j in types:
                Rij = graph.get_relation_matrix(i,j)
                if Rij is not None:
                    self.R[(i,j)] = Rij

    def build_S(self):
        S = dict()
        for (i,j) in self.R:
            Rij = self.R[(i,j)]

            dij = np.sum(Rij, axis=1)
            dji = np.sum(Rij, axis=0)

            dij = 1.0/(dij**.5)
            dji = 1.0/(dji**.5)

            S[(i,j)] = np.dot(np.diag(dij) , Rij )
            S[(i,j)] = np.dot(S[(i,j)] , np.diag(dji))

        return S

    def initialize(self):
    # ---------------------------------------------------------------- #
    # Metodo para inicializar as variaveis auxiliares para a iteracao do 
    # metodo
    # ---------------------------------------------------------------- #
        m = self.graph.get_m()
        types = self.graph.get_types()
        K = self.graph.get_K()
        self.f = dict()
        self.y = dict()
        labels = self.graph.get_labels()

        for i in types:
            ni = self.graph.get_n(i)
            fi = np.zeros( (ni,K) )

            for p in range(ni):
                classi = self.graph.get_class(i,p)

                if classi is not None:
                    ci = labels.index(classi)
                    fi[p,ci] = 1
                    self.y[ (i,p) ] = np.zeros(K)
                    self.y[ (i,p) ][ci] = 1

            self.f[i] = fi
        
        self.build_relation_matrix()
        self.S = self.build_S()
        self.labels = labels

    def iterate_f(self):
        m = self.graph.get_m()  
        K = self.graph.get_K()
        f1 = dict()
        alpha = self.alpha
        gamma = self.gamma
        f = self.f
        types = self.graph.get_types()

        # Iteracao para todos os tipos de objetos
        for i in types:
            ni = self.graph.get_n(i)
            f1[i] = np.zeros( (ni,K) )
            over = 0

            # Iteracao para cada objeto do tipo i
            for p in range(ni):
                # Se o objeto p do tipo i for rotulado esta restricao estara
                # ativa 
                y = self.y.get((i,p), None)
                if y is not None: 
                    f1[i][p,:] = alpha*y
                    over += alpha

            # Se houver ligacoes entre os objetos do tipo i com ele
            # mesmo a seguinte parcela contribuira
            Sii = self.S.get((i,i), None)
            if Sii is not None:
                f1[i] += +2*gamma*np.dot(Sii,f[i])
                over += 2*gamma

            for j in types:
                Sij = self.S.get((i,j), None)
                if Sij is not None:
                    f1[i] = f1[i]+gamma*np.dot(Sij,f[j])
                    over+= gamma

        return f1

    # ---------------------------------------------------------------- #
    # Main method
    # ---------------------------------------------------------------- #
    def run(self, max_it = 100):
        t = 0
        m = self.graph.get_m()
        types = self.graph.get_types()

        # Passo 0
        self.initialize()
        f1 = self.f

        # Passo 1
        while t < max_it :
            self.f = f1 
            f1 = self.iterate_f()
            t += 1

        self.f = f1
        # Passo 3
        c = dict()
        for i in types:
            ni = self.graph.get_n(i)
            c[i] = [ -1 ]*ni
            
            for p in range(ni):
                c[i][p] = np.argmax( self.f[i][p,:] )

        return c
