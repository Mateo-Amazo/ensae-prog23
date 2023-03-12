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

        if not self.graph:
            output = "The graph is empty"
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):

        nodes = self.nodes
        if node1 not in nodes :
            self.nb_nodes += 1
            self.nodes += [node1]
        if node2 not in nodes :
            self.nb_nodes += 1
            self.nodes += [node2]
      
        if node1 in self.graph:
            if not ((node2, power_min, dist) in self.graph[node1]):
                self.graph[node1] += [(node2, power_min, dist)]
        else:
            self.graph[node1] = [(node2, power_min, dist)]
        if node2 in self.graph:
            if not ((node1, power_min, dist) in self.graph[node2]):
                self.graph[node2] += [(node1, power_min, dist)]
        else:
            self.graph[node2] = [(node1, power_min, dist)]

    def connected_components_p(self, p):

        "Cette fonction prend en entrée un graph et le power p que le camion possède pour parcourir les composantes connexes"
        "Elle renvoie les composantes connexes du graphe pour un camion qui aurait un power p"

        nodes = self.nodes
        composantes_connexes = []
        bool = 0  
        
        for node in nodes :

            "On parcourt toutes les nodes du graphe"

            for val in composantes_connexes:
                if node in val:
                    bool = 1
            
            "On utilise un booleen pour vérifier qu'on ne créé pas une composante connexe qui existe déjà"

            if bool == 0:
                composantes_connexes += [self.voisins_p(node, [node], p)]

                "Pour chaque sommet qui n'appartient pas à une composante connexe déjà existante, on rajoute ce sommets et tous les sommets qui lui sont reliés avec un power inférieur à p"

        return composantes_connexes

    def voisins_p(self, node, voisin, p):

        "Cette fonction récursive prend en entre une node qui sera notre point de départ, une liste de voisins (qui contient les nodes que nous avons parcourues pour l'instant dans notre parcours en profondeur) et un power p"
        "Elle renvoie donc toutes les nodes accessibles depuis notre node avec un power p"
        
        adj = self.graph[node]
        if adj == []:
            return voisin

        "Si la node a une liste d'adjacence vite alors la composante connexe la contenant est réduite à [node]"

        for val in adj:

            if not (val[0] in voisin) and val[1] <= p:
                "On vérifie que le sommet n'a pas déjà été parcouru et que nous pouvons l'atteindre avec notre power p"
                
                voisin = self.voisins_p(val[0], voisin + [val[0]], p)
        
        return voisin

    def get_path_with_power(self, src, dest, p):

        "Cette fonction prend en argument une node de départ, une node d'arrivée et le power p que notre camion possède pour tenter de faire le trajet"
        "Elle renvoie la distance minimale qu'on doit parcourir avec un power p pour passer de src à dest"

        sommets = self.voisins_p(src, [], p)
        "nodes accessibles avec un power p"

        if dest not in sommets:
            "Si notre destination n'est pas dans les sommets atteignable avec un power p, on ne peut pas calculer la distance minimale entre src et dest avec un power p"
            return -1
        
        return self.aux_dijkstra(src, dest, sommets)

    def aux_dijkstra(self, src, dest, sommets):
        
        "Cette fonction prend en entrée une node de départ, une node d'arrivée et la composante connexe les contenants"
        "Cette fonction auxilliaire execute l'algorithme de dijkstra et renvoie la distance minimale entre la node de départ et d'arrivée dans le sous-graphe 'sommets' "

        d = [self.dist(src,dest2) for k,dest2 in enumerate(sommets)]
        "d vecteur de distance"
        F = retire(sommets, src)
        
        bijection = {}
        for i, val in enumerate(sommets):
            bijection[val] = i
        "Ce dictionnaire sert juste à numéroter les nodes de sommets de 0 à len(sommets)-1"

        minarg = F[0]
        minu = np.inf

        while F != []:
            minarg = F[0]
            for val in F:
                minu = np.inf
                if d[bijection[val]] < minu:
                    minarg = val
                    minu = d[bijection[val]]
            F = retire(F, minarg)
            for v in sommets:
                i = bijection[v]
                j = bijection[minarg]
                d[i] = min(d[i], d[j] + self.dist(v, minarg))
        "Cette boucle execute l'algorithme de dijkstra"

        "La distance minimale se trouve dans le vecteur de distance d"
        return d[bijection[dest]]

    def dist(self, val, val2):

        "Prend en argument 2 nodes et renvoie la distance entre les 2 et np.inf si les nodes ne sont pas reliées par une arrête"

        if val == val2:
            return 0
        adj = self.graph[val]
        for k in adj:
            if k[0] == val2:
                return k[2]
        return np.inf

    def connected_components(self):
        "Comme nous avons déjà une fonction qui renvoie les composantes connexes selon un power p, pour avoir les composantes connexes indépendemment du power p, il suffit d'avoir un power p infini (= notre camion peut parcourir toutes les arretes"
        return self.connected_components_p(np.inf)

    def connected_components_set(self): 
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))

    def min_power(self, src, dest):

        "Cette fonction prend en argument 2 nodes et renvoie le power minimal pour passer d'une node à l'autre grace à une dichotomie"
        power = np.inf
        d = self.get_path_with_power(src, dest, power)

        if d == -1:
            "On se souvient que si get_path_with_power renvoie une distance de -1 alors le trajet n'existe pas"
            "Dans ce cas là, on renvoie un vecteur du type (dest,np.inf,np.inf) car power = np.inf à ce moment là"
            "Ce vecteur n'a aucune chance d'exister dans un graphe normal et nous permet de trouver les cas problématiques"
            return (dest, power, power)


        "Pour faire une dichotomie nous avons besoin de 2 valeurs entre lesquelles l'executer"
        power = 1
        n = 0
        d = self.get_path_with_power(src, dest, power)
        while d == -1:
            power *= 2
            n += 1
            d = self.get_path_with_power(src, dest, power)
        inf = power//2
        sup = power
        "Les 9 lignes qui précèdent nous permettent de trouver le n tel que min_power soit entre 2**(n-1) et 2**n"
        "En effet comme 2**(n-1) ne suffit pas pour passer de src à dest et que 2**n suffit, min_power est nécessairement entre les 2"
        "La raison pour laquelle nous faisons ceci avec des puissances de 2 est pour une question de complexité de l'algorithme"
        "En effet une recherche en incrémentant seulement de 1 (au lieu de multiplier par 2) aurait pris un temps important dans le cas où min_power est très élevé, on passe d'une complexité linéaire à une complexité en log2"

        "On fait ensuite une dichotomie entre ces 2 valeurs"
        while (sup-inf > 1):
            mid = (inf+sup)//2
            if self.get_path_with_power(src, dest, mid) >= 0:
                sup = mid
            else:
                inf = mid
        return (dest, d, sup)

    def kruskal(self):

        "Cette fonction execute l'algorithme de kruskal sur un graphe que l'on suppose connexe"
        dic = self.graph
        nodes = self.nodes
        arretes = []
        g_mst = Graph([node for node in nodes])

        for src in nodes :
            adj = dic[src]
            for dest in adj:
                if src < dest[0]:
                    arretes += [(src, dest[0], dest[1])]
        arretes = sorted(arretes, key=lambda x: x[2])
        "On créé la liste des arretes en faisant attention à ne pas faire apparaître 2 fois une même arrete (à l'aide la fonction de comparaison '>') pour éviter trop de calculs par la suite et réduire la complexité"

        for arrete in arretes:
            node1 = arrete[0]
            node2 = arrete[1]
            
            vois = g_mst.voisins_p(node1, [node1], np.inf)
            if node2 not in vois:
                "On vérifie que l'on ne créé pas de cycles"
                "En effet on créé un cycle si node2 est dans la composante connexe contenant node1 dans le graphe g_mst"

                power_min = arrete[2]
                g_mst.add_edge(node1, node2, power_min)

        return g_mst

    def power_min(self, src, dest):
        
        "Renvoie le power minimal pour passer de src à dest (en utilisant le graphe formé par l'algorithme de kruskal) à l'aide d'une fonction auxilliare voisins_power"
        g_mst = self.kruskal()
        
        voisin_power = g_mst.voisins_power(src, [(src, 0)], 0)
        "voisins_power renvoie la liste des nodes du graphe et le power minimal qu'il faut pour atteindre chacune d'entre elles"

        for val in voisin_power :
            if val[0] == dest :
                return val[1]
        return -1
    
    "Analysons désormais la complexité de power_min :"
    "Dans un premier temps nous calculons l'abre couvrant de power minimal associer à g grace à l'algorithme de kruskal"
    
    "a) Complexité de Kruskal :"
    "kruskal a (dans notre implémentation) une complexité en O(n**2) avec ici n = g.nb_nodes"
    "En effet le tri des arretes se fait en O(nlog(n))"
    "Puis nous effectuons un parcours en profondeur pour trouver tous les sommets reliés à notre src pour vérifier que nous ne créons pas de cycle "
    "Un parcours en profondeur est en O(n+m) (n nb_nodes et m = nb_edges de g_mst ici), or durant notre execution, g_mst a un nombre d'arrete majoré par n-1"
    "Donc la complexité du parcours en profondeur est de O(2n-1) = O(n)"
    "Nous effectuons ce parcours en profondeur pour chaque arrete de g, on le fait donc g.nb_edges fois"
    "Kruskal est donc en complexité O(g.nb_nodes * g.nb_edges)"

    "b) complexité de voisins_power"
    "Puis nous executons voisins_power qui en tant que parcours en profondeur a une complexité de O(n) (même démo)"

    "Conclusion"
    "L'algorithme que nous avons implémenté est en complexité O(g.nb_nodes * g.nb_edges)"
    "Néanmoins cette complexité est dûe à des parcours en profondeur, il me semble qu'union_find permet d'obtenir une complexité en nlog(n), la hauteur d'un arbre couvrant étant en log(nb_nodes)"

    def voisins_power(self, src, voisin, power):
        
        "Cette fonction auxilliaire effectue un parcours en profondeur et stocke pour chaque node le power qu'il a fallut pour l'atteindre"
        "La structure du graphe que renvoie l'algorithme de kruskal nous garantit que le power trouvé est bien le power minimal"
        adj = self.graph[src]

        if adj == []:
            return voisin
        for val in adj:
            dest = val[0]
            booleen = 0
            for couple in voisin:
                if couple[0] == dest:
                    booleen = 1
            if booleen == 0:
                voisin = self.voisins_power(val[0], voisin + [(val[0], max(val[1], power))], max(val[1], power))
        return voisin


def graph_from_file(filename):
    "Prend en entrée une adresse de fichier et renvoie un graphe"

    f = open(filename)
    mots = f.readline().split()

    n = int(mots[0])
    m = int(mots[1])
    g = Graph([k for k in range(1, n+1)])
    for k in range(m):
        mots = f.readline().split()
        if len(mots) == 3:
            g.add_edge(int(mots[0]), int(mots[1]), int(mots[2]))
        else:
            g.add_edge(int(mots[0]), int(mots[1]), int(mots[2]), int(mots[3]))
        g.nb_edges += 1
    f.close()
    return g

def retire(liste, x):
    "Prend en entrée une liste et renvoie une copie où l'on a retiré l'élément x"

    res = []
    for val in liste:
        if val != x:
            res += [val]
    return res

def test_temps(x = "1", data_path = "input/") :

    routes_file_name = "routes." + str(x[-1]) + ".in"
    network_file_name = "network." + str(x) + ".in"

    g = graph_from_file(data_path + network_file_name)
    f = open(data_path + routes_file_name)
    g_mst = g.kruskal()

    sum_timek = 0
    sum_timed = 0

    n = int(f.readline())
    for k in range(1) :

        mots = f.readline().split()
        src = int(mots[0])
        dest = int(mots[1])

        #t1 = time.time()
        #a = g.min_power(src,dest)
        #t2 = time.time()
        #sum_timed += t2-t1


        t1 = time.time()
        a = g_mst.voisins_power(src, [(src, 0)], 0)
        t2 = time.time()
        sum_timek += t2-t1

    f.close()
    return {"kruskal" : sum_timek/n, "dichotomie" : sum_timed/n}

# Espace de test


test_temps(x="2")

data_path = "input/"
file_name = "network.1.in"

g = graph_from_file(data_path + file_name)
print(g)

g.min_power(17,15)
g.power_min(17,15)



g_mst = g.kruskal()
g_mst.voisins_power(17, [(17, 0)], 0)

print(g_mst)
g.connected_components_p(100)

g_mst.power_min(17,15)

g2 = Graph(["Paris","Palaiseau"])
g2.add_edge("Paris","Palaiseau",100)
g2.connected_components()
