import sys 
sys.path.append("D:\Travail\ENSAE 1A\Projet de programmation\ensae-prog23\delivery_network")
from graph import Graph, graph_from_file
import random as rd
B = 25*(10**9)
data_path = "input/"


def recup_camions(x, data_path = "/home/onyxia/ensae-prog23-1/input/"):

    res = []
    f = open(data_path + "trucks."+str(x)+".in")
    n = int(f.readline())
    print(type(n))
    for i in range(n):
        mots = f.readline().split()
        res += [(int(mots[0]), int(mots[1]))]
    f.close()
    res = sorted(res, key=lambda x: x[0])
    return res

def recup_profits(x, data_path="/home/onyxia/ensae-prog23-1/input/"):

    res = []
    routesin = open(data_path + "routes." + str(x) + ".in")
    routesout = open(data_path + "routes." + str(x) + ".out")
    n = int(routesin.readline())
    for i in range(n):
        mots = routesin.readline().split()
        mots2 = routesout.readline().split()
        res += [[int(mots[-1]), int(mots2[0]),0]]
    routesin.close()
    routesout.close()
    return res

def opti(x, n_it_max, B):

    liste_profits = recup_profits(x)
    liste_camions = recup_camions(x)

    camions, profits, couts= aux_opti(liste_profits, liste_camions)
    t = camions["nb_camions"]

    n_it = 0
    while n_it < n_it_max:
        n_it += 1
        p = rd.randint(0, t-1)

        couts_temp = 0
        profits_temp = 0
        camions_temp = []

        for k in range(p):
            p2 = rd.randint(0,t-1)
            while camions[p2] == []:
                p2 = rd.randint(0,t-1)
            aux = camions[p2]
            length = len(aux)
            camions_temp += [(p2,rd.randint(0,length-1))]
        



def aux_opti(liste_profits, liste_camions, budget=B):
    couts = 0
    profits = 0

    m = len(liste_profits)
    n = len(liste_camions)
    res = dict([(l,[]) for l in range(n)])
    bij = bijection(n)
    nb_camions = 0

    cpt = 0
    booleen = 0
    while booleen == 0 and cpt != m :

        cpt = 0
        p = bij[0]
        prix = liste_camions[p][1]

        bc = budget-couts
        i = 1
        while prix > bc and i < n :
            p = bij[i]
            prix = liste_camions[p][1]
            i += 1

        if couts + prix <= budget:
            power = liste_camions[p][0]
            k = 0
            aux = liste_profits[k][2]
            booleen2 = (liste_profits[k][1] > power or aux == 1)
            if aux == 1:
                cpt += 1
            while k < m and booleen2 :
                k += 1
                if k < m :
                    aux = liste_profits[k][2]
                    booleen2 = (liste_profits[k][1] > power or aux == 1)
                    if aux == 1 :
                        cpt += 1

            if k < m :
                liste_profits[k][2] = 1
                profit = liste_profits[k][0]
                res[p] += [(profit,prix)]
                profits += profit
                couts += prix
        else :
            booleen = 1

        nb_camions += 1
    res["nb_camions"] = nb_camions
    return res, profits, couts

res, profits, couts = aux_opti(recup_profits(3,data_path),recup_camions(2,data_path))
print(profits)

def bijection(n):
    res = []
    for k in range(n):
        p = rd.randint(0,n-1)
        while p in res:
            p = rd.randint(0,n-1)
        res += [p]
    return res
