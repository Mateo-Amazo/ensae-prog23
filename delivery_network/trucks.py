import sys 
sys.path.append("D:\Travail\ENSAE 1A\Projet de programmation\ensae-prog23\delivery_network")
from graph import Graph, graph_from_file
import random as rd
import time
B = 25*(10**9)
data_path = "input/"


def recup_camions(x, data_path = "/home/onyxia/ensae-prog23-1/input/"):

    res = []
    f = open(data_path + "trucks."+str(x)+".in")
    n = int(f.readline())
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

def opti(x, y, n_it_max, budget, data_path="/home/onyxia/ensae-prog23-1/input/"):

    liste_profits2 = recup_profits(x, data_path)
    liste_camions = recup_camions(y, data_path)

    camions, profits, couts, liste_profits = aux_opti_init(x,y,liste_profits2,data_path,budget)
    print("init done")
    t = len(camions)
    n = len(liste_camions)

    n_it = 0
    while n_it < n_it_max:
        print(n_it)
        n_it += 1
        p = rd.randint(0, n-1)
        
        liste_profits_aux = liste_profits
        couts_aux = 0
        camions_aux = []

        for k in range(p):
            p2 = rd.randint(0,t-1)
            while camions[p2] == []:
                p2 = rd.randint(0,t-1)
            aux = camions[p2]
            length = len(aux)
            camions_aux += [(p2,rd.randint(0,length-1))]

        for val in camions_aux:
            (a,b) = val
            aux = camions[a]
            couts_aux += aux[b][1]
            liste_profits_aux[aux[a][2]][2] = 0
        
        budget_aux = budget - couts + couts_aux

        camions_temp, profits_temp, couts_temp, liste_profits_temp = aux_opti(liste_profits_aux, liste_camions, budget_aux)

        if profits_temp > profits :
            camions = camions_temp
            profits = profits_temp
            couts = couts_temp
            liste_profits = liste_profits_temp

    return profits

def bijection(n):
    res = []
    for k in range(n):
        p = rd.randint(0,n-1)
        while p in res:
            p = rd.randint(0,n-1)
        res += [p]
    return res

def aux_opti(liste_profits, liste_camions, budget=B):
    couts = 0
    profits = 0

    m = len(liste_profits)
    n = len(liste_camions)
    res = dict([(l,[]) for l in range(n)])
    bij = bijection(n)

    cpt = 0
    cpt2 = 0
    booleen = 0
    while booleen == 0 and cpt != m and cpt2 != n:

        cpt = 0
        p = bij[0]
        prix = liste_camions[p][1]

        bc = budget-couts
        i = 1
        while prix > bc and i < n :
            p = bij[i]
            prix = liste_camions[p][1]
            i += 1
            if i > cpt2:
                cpt2 = i

        if couts + prix <= budget and i < n:
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
                res[p] += [(profit,prix,k)]
                profits += profit
                couts += prix
                cpt2 = 0 
        else :
            booleen = 1
    return res, profits, couts, liste_profits

def utiliteprix_write(x,y,data_path = "/home/onyxia/ensae-prog23-1/input/"):
    liste_profits = recup_profits(y, data_path)
    liste_camions = recup_camions(x, data_path)
    res = []
    for k,val in enumerate(liste_camions) :
        power,prix = val
        max_profit = 0        
        for val2 in liste_profits:
            profit,power_min,z = val2
            if power_min <= power and profit > max_profit:
                max_profit = profit
        res += [(prix, profit, profit/prix)]
    res = sorted(res,key=lambda x: x[2], reverse= True)
    res2 = []
    val = res[-1]
    for val2 in res:
        if val2 != val:
            res2 = res2 + [str(val2[0]) + " " + str(val2[1]) + " " + str(val2[2]) + " \n"]
        else:
            res2 = res2 + [str(val2[0]) + " " + str(val2[1]) + " " + str(val2[2])]
    res2 = [str(len(res2))+"\n"] + res2
    w = open("trucks." + str(x) + "and" + str(y) + ".out","a")
    w.writelines(res2)
    w.close()

for i in range(3):
    for j in range(1,3):
        utiliteprix_write(i,j,data_path)

def utiliteprix(x,y,data_path = "/home/onyxia/ensae-prog23-1/input/"):
    liste_profits = recup_profits(y, data_path)
    liste_camions = recup_camions(x, data_path)
    res = []
    for k,val in enumerate(liste_camions) :
        power,prix = val
        max_profit = 0        
        for val2 in liste_profits:
            profit,power_min,z = val2
            if power_min <= power and profit > max_profit:
                max_profit = profit
        res += [(prix, profit)]
    res = sorted(res,key=lambda x: x[1]/x[0], reverse=True)
    return res

def utiliteprix_opti(x,y,data_path = "/home/onyxia/ensae-prog23-1/input/"):
    f = open(data_path + "trucks." + str(x) + "and" + str(y) + ".out")
    n = int(f.readline())
    res = []
    for k in range(n):
        mots = f.readline().split()
        res = res + [(int(mots[0]),int(mots[1]))]
    f.close()
    return res

def aux_opti_init(x,y,liste_profits, data_path ="/home/onyxia/ensae-prog23-1/input/", budget=B):
    liste_camions = utiliteprix_opti(x,y,data_path)
    m = len(liste_profits)
    n = len(liste_camions)

    couts = 0
    profits = 0

    m = len(liste_profits)
    n = len(liste_camions)
    res = dict([(l,[]) for l in range(n)])

    p = 0
    while p != n:

        profit, prix = liste_camions[p]

        bc = budget-couts
        if prix <= bc:
            couts += prix
            profits += profit
        else:
            p += 1

    return res, profits, couts, liste_profits

utiliteprix_opti(1,1,data_path)
B = 25*(10**9)
res, profits, couts, liste_profits = aux_opti_init(2,2,recup_profits(2,data_path),data_path,B)
print(res)
