import time
import numpy as np


class Graph:
    def __init__(self, nodes=[]):

        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
    
    def __str__(self):

        if not self.graph:
            output = "The graph is empty"
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):
  

        if not ((node2, power_min, dist) in self.graph[node1]):
            self.graph[node1] += [(node2, power_min, dist)]
            self.nb_edges += 1
            self.graph[node2] += [(node1, power_min, dist)]
            self.nb_edges += 1

            self.edges += [(node1,node2,power_min)]


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
                composantes_connexes += [self.voisins_p(node, [node], p, dict([(nod,0) for nod in self.nodes]))]

                "Pour chaque sommet qui n'appartient pas à une composante connexe déjà existante, on rajoute ce sommets et tous les sommets qui lui sont reliés avec un power inférieur à p"

        return composantes_connexes

    def voisins_p(self, node, voisin, p, dic):

        "Cette fonction récursive prend en entre une node qui sera notre point de départ, une liste de voisins (qui contient les nodes que nous avons parcourues pour l'instant dans notre parcours en profondeur) et un power p"
        "Elle renvoie donc toutes les nodes accessibles depuis notre node avec un power p"
        adj = self.graph[node]
        if adj == []:
            return voisin

        "Si la node a une liste d'adjacence vite alors la composante connexe la contenant est réduite à [node]"

        for val in adj:

            if dic[val[0]] == 0 and val[1] <= p:
                "On vérifie que le sommet n'a pas déjà été parcouru et que nous pouvons l'atteindre avec notre power p"
                dic[val[0]] = 1
                voisin = self.voisins_p(val[0], voisin + [val[0]], p, dic)
        
        return voisin

    def get_path_with_power(self, src, dest, p):

        "Cette fonction prend en argument une node de départ, une node d'arrivée et le power p que notre camion possède pour tenter de faire le trajet"
        "Elle renvoie la distance minimale qu'on doit parcourir avec un power p pour passer de src à dest"

        sommets = self.voisins_p(src, [], p, dict([(nod,0) for nod in self.nodes]))
        "nodes accessibles avec un power p"

        if dest not in sommets:
            "Si notre destination n'est pas dans les sommets atteignable avec un power p, on ne peut pas calculer la distance minimale entre src et dest avec un power p"
            return -1
        
        return self.aux_dijkstra(src, dest, sommets)
    
    "Plusieurs éléments interviennent dans la complexité de cette fonction :"
    "1) Dans un premier temps, la fonction voisins_p, celle-ci execute un parcours en profondeur"
    "Or, on sait qu'un parcours en profondeur a une complexité en O(n+m) car on ne traite qu'une seule fois chaque arrete et node"
    "2) Dans un deuxième temps, comme nous avons décidé de faire la question 5 nous executons l'algorithme de dijkstra"
    "la fonction aux_dijkstra execute comme son nom l'indique l'algorithme de dijkstra"
    "Or on sait que celle-ci a une complexité de O(nlog(n))"
    "Néanmoins pour l'initialiser nous avons besoin d'un vecteur de distance dont la création est en O(n^2)"
    "3) Nous avons donc un résultat en O(n^2)"

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
        "Comme nous avons déjà une fonction qui renvoie les composantes connexes selon un power p, pour avoir les composantes connexes indépendemment du power p, il suffit d'avoir un power p infini (= notre camion peut parcourir toutes les arretes)"
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
        return (dest, sup, d)

    def kruskal(self):

        "Cette fonction execute l'algorithme de kruskal sur un graphe que l'on suppose connexe"
        g_mst = Graph(self.nodes)
        arretes = sorted(self.edges, key=lambda x: x[2])
        "On créé la liste des arretes triées, on a fait attention précedemment à ce que dans self.edges chaque arrête n'apparaisse qu'une fois (càd que si une arrete de a vers b existe, celle de b vers a avec le même power n'apparaîtra pas)"

        dic = dict([(node, [node, 0]) for node in g_mst.nodes])

        def find(x):
            while x != dic[x][0]:
                x = dic[x][0]
            return x
        def union(x, y):
            rx = find(x)
            ry = find(y)
            rank_rx = dic[rx][1]
            rank_ry = dic[ry][1]

            if rank_rx > rank_ry:
                dic[ry][0] = rx
            else:
                dic[rx][0] = ry
                if rank_rx == rank_ry:
                    dic[ry][1] += 1
        "On créé les fonctions union et find du pdf fourni"

        for arrete in arretes:
            x = arrete[0]
            y = arrete[1]

            if find(x) != find(y):

                power_min = arrete[2]
                g_mst.add_edge(x, y, power_min)
                union(x, y)
        "On execute kruskal grâce aux fonctions précédentes"
        racine = find(g_mst.nodes[0])
        "On renvoie la racine aussi, celà servira pour la fonction ci-dessous"
        return g_mst, racine

    def min_poweraux(self, racine):
        "La fonction prend en entrée un arbre couvrant sous forme de graphe et sa racine"
        nodes = self.nodes
        parents = dict([(node, (-1, -1)) for node in nodes])
        parents[racine] = (racine,0)
        prof = dict([(node, 0) for node in nodes])

        def dictparents(g, node, prof2):

            dic2 = g.graph
            adj = dic2[node]
        
            for arrete in adj:
                node2 = arrete[0]
                if parents[node2] == (-1, -1):
                    parents[node2] = (node, arrete[1])
                    prof[node2] = prof2
                    dictparents(g,node2, prof2+1)

        dictparents(self,racine, 1)
        
        "Elle renvoie 2 dictionnaires :"
        "Le premier est un dictionnaire qui à chaque node associe un couple (parent,power) avec power le power nécessaire pour passer au parent dans le graphe"
        "Le deuxième est celui des profondeurs de chacune des nodes dans l'arbre"
        return parents, prof

def min_power2(src, dest, parents, prof):

        "Comme les fonctions précédentes nous permettent de trouver le dictionnaire des parents et des profondeurs associées, il nous suffit maintenant de trouver le premier parent commun entre les 2 sommets"
        "A chaque fois que l'on remonte l'arbre on rajoute le power qui nous a fallut pour remonter"
        power = 0
        prof_src = prof[src]
        prof_dest = prof[dest]

        mprof = 0
        pprof = 0

        if prof_src > prof_dest:
            pprof = src
            mprof = dest
        else:
            pprof = dest
            mprof = src

        n = prof[pprof]
        m = prof[mprof]

        booleen = 0
        if n != m :
            booleen = 1

        while n != m:
            power += parents[pprof][1]
            pprof = parents[pprof][0]
            n -= 1
        
        if booleen == 1 :
            power += parents[pprof][1]

        for i in range(n):
            pprof = parents[pprof][0]
            mprof = parents[mprof][0]
            power += parents[pprof][1] + parents[mprof][1]
        
        return power

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
            g.add_edge(int(mots[0]), int(mots[1]), int(mots[2]), float(mots[3]))
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

    "Prend en entrée le numéro du fichier network que l'on veut utiliser et le path dans lequel le trouver et renvoie le temps qu'il faut pour calculer tous les power min des trajets dans le fichier route correspondant"

    routes_file_name = "routes." + str(x) + ".in"
    network_file_name = "network." + str(x) + ".in"

    g = graph_from_file(data_path + network_file_name)
    f = open(data_path + routes_file_name)
    g_mst, racine = g.kruskal()
    parents, prof = g_mst.min_poweraux(racine)

    sum_timek = 0

    n = int(f.readline())
    print(n)
    for k in range(n) :

        mots = f.readline().split()
        src = int(mots[0])
        dest = int(mots[1])

        t1 = time.time()
        a = min_power2(src,dest,parents,prof)
        t2 = time.time()
        sum_timek += t2-t1

    f.close()
    return sum_timek

def question_15() :

    res = ["0" for k in range(10)]
    w = open("delivery_network/Résultats question 15","a")
    
    for k in range(1,10) :
        res[k-1] = "fichier " + str(k) + ": " + str(test_temps(str(k))) + "\n"
    
    w.writelines(res)
    w.close()


# Espace de test

question_15()
test_temps(x = "9")

g = graph_from_file("input/" + "network.9.in")

g_mst, racine = g.kruskal()
parents, prof = g_mst.min_poweraux(racine)
print(parents)

min_power2(111142, 193829,parents,prof)

g.min_power(20,11)[-2]

print(g_mst)
g.connected_components_p(100)

g_mst.power_min(17,15)

g2 = Graph(["Paris","Palaiseau"])
g2.add_edge("Paris","Palaiseau",100)
g2.connected_components()

dict([(nod,0) for nod in g.nodes])