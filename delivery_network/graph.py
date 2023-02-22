import time
import os
import numpy as np
import matplotlib.pyplot as plt
import random as rd

class Graph:

    def __init__(self, nodes=[]):

        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):

        if node1 in self.graph : 
            
            if not ((node2,power_min,dist) in self.graph[node1]) :
                self.graph[node1] += [(node2,power_min,dist)]
        else :
            self.graph[node1] = [(node2,power_min,dist)]

        if node2 in self.graph : 
            if not ((node1,power_min,dist) in self.graph[node2]) :
                self.graph[node2] += [(node1,power_min,dist)]
        else :
            self.graph[node2] = [(node1,power_min,dist)]  

    def get_path_with_power(self, src, dest, power):
        
        dic = self.graph
        adj = dic[src]
        trajets = []

        for val in adj :
            
            if val[1] <= power :
                trajets += ([val[0]],val[1],val[2],1)
        
        trajets = self.aux_get_path(dest,power,trajets)

        bool = 0
        d = -1

        for val in trajets :

            if (val[0][-1] == dest) and (val[1] <= power) and (bool == 1) :
                bool = 1
                d = val[2]
            elif (val[0][-1] == dest) and (val[1] <= power) :
                if val[2] < d :
                    d = val[2]
        
        return d


    def aux_get_path(self,dest,power,trajets) : #Trajets, liste de trajets du type ([vecteur de nodes],power du trajet, distance du trajet,booleen)
        
        dic = self.graph
        trajets2 = []
        bool = 0

        for trajet in trajets :

            if trajet[-1] == 1 :
                
                nodes = trajet[0]
                powertrajet = trajet[1]
                powerdist = trajet[2]

                aux = nodes[-1]
                adj = dic[aux]


                for val in adj :
                        
                    if val != dest :
                        if (val[1] + powertrajet > power) or (val == dest) :
                            trajets2 += (nodes+[val[0]],powertrajet + val[1],powerdist + val[2],0)
                            
                        else :
                            trajets2 += (nodes+[val[0]],powertrajet + val[1],powerdist + val[2],1)
                            bool = 1

        if bool == 0 :
            return trajets2
        
        return self.aux_get_path(dest,power,trajets2)

    def connected_components(self):
        dic = self.graph
        n = len(dic)
        res = []
        bool = 0 #Simple booléen

        k = 0
        while k < n :
            bool = 0

            for val in res : #On vérifie qu'on ne créé pas une composante connexe qui existe déjà
                if k in val :
                    bool = 1
            
            if bool == 0 :
                res  +=  [self.voisins(k,[k])]
            k += 1
        
        return res

    def voisins(self,k,voisin) :
        adj = self.graph[k]
        
        if adj == [] :
            return voisin

        for val in adj :
            if not(val[0] in voisin) :
                
                voisin = self.voisins(val[0],voisin + [val[0]])
        

        return voisin

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    

    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        power = np.inf
        d = self.get_path_with_power(src,dest,power)

        if d == -1 :
            return ((dest,power,power),power) #Renvoie un vecteur spécial si le passage n'existe pas

        power = 1 #Je considère ici que le power minimum pour traverser n'importe quel trajet est de 1, j'aurai pu traiter le cas 0 à part.
        n = 0

        d = self.get_path_with_power(src,dest,power)

        while d == -1 :
            power *= 2
            n += 1
            d = self.get_path_with_power(src,dest,power)
        
        inf = power//2
        sup = power

        while (sup-inf > 1) :
            mid = (inf+sup)//2
            if self.get_path_with_power(src,dest,mid) >= 0 :
                sup = mid
            else : 
                inf = mid

        return ((dest,d,sup),sup)


def graph_from_file(filename):

    f = open(filename)
    mots = f.readline().split()

    n = int(mots[0])
    m = int(mots[1])

    g = Graph([k for k in range(n)])

    for k in range(m) :
        mots = f.readline().split()

        if len(mots) == 3 :
            g.add_edge(int(mots[0]),int(mots[1]),int(mots[2]))
        else :
            g.add_edge(int(mots[0]),int(mots[1]),int(mots[2]),int(mots[3]))
    
    f.close()

    return g

# Espace de test

