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

def utiliteprix_write(x,y,data_path = "/home/onyxia/ensae-prog23-1/input/"):
    liste_profits = recup_profits(y, data_path)
    liste_camions = sorted(recup_camions(x, data_path),key = lambda x : x[1])
    n = len(liste_profits)
    res = []
    for k,val in enumerate(liste_profits):
        profit, min_power, z = val
        i = 0
        booleen = False    
        while i < n and not booleen:
            val2 = liste_camions[i]
            power, prix = val2
            if min_power <= power and z != 1:
                min_prix = prix
                booleen = True
            i += 1
        if booleen :
            liste_profits[k][-1] = 1
            res += [(profit, min_prix, k, profit/min_prix)]
    res = sorted(res,key=lambda x: x[-1], reverse= True)
    res2 = []
    val = res[-1]
    for val2 in res:
        if val2 != val:
            res2 = res2 + [str(val2[0]) + " " + str(val2[1]) + " " + str(val2[2]) + " \n"]
        else:
            res2 = res2 + [str(val2[0]) + " " + str(val2[1]) + " " + str(val2[2])]
    res2 = [str(len(res2))+"\n"] + res2
    w = open(data_path + "trucks." + str(x) + str(y) + ".out","a")
    w.writelines(res2)
    w.close()


utiliteprix_write(2,9,data_path)

def utiliteprix(x,y,data_path = "/home/onyxia/ensae-prog23-1/input/"):
    f = open(data_path + "trucks." + str(x) + str(y) + ".out")
    n = int(f.readline())
    res = []
    for k in range(n):
        mots = f.readline().split()
        res = res + [[int(mots[0]),int(mots[1]),0]]
    f.close()
    return res

def opti(x, y, n_it_max, budget, data_path="/home/onyxia/ensae-prog23-1/input/"):

    camions, profits, couts = aux_opti_init(x, y, data_path, budget)
    t = len(camions)

    n_it = 0
    while n_it < n_it_max:
        print(profits)
        p = rd.randint(0, t-1)
        remplace = []
        for k in range(p):
            remplace += [rd.randint(0,t-1)]

        couts_aux = 0
        camions_aux = camions
        profits_aux = 0

        for p in remplace:
            camions_aux[p][2] = 0
            couts_aux += camions[p][0]
            profits_aux += camions[p][1]
        
        budget_aux = budget - couts + couts_aux

        camions_temp, profits_temp, couts_temp = aux_opti(camions_aux, budget_aux)


        if profits_temp > profits_aux :
            camions = camions_temp
            profits = profits-profits_aux + profits_temp
            couts = couts - couts_aux + couts_temp

        n_it += 1

    return profits

def bijection(n):
    res = []
    for k in range(n):
        p = rd.randint(0,n-1)
        while p in res:
            p = rd.randint(0,n-1)
        res += [p]
    return res

def aux_opti_init(x, y, data_path ="/home/onyxia/ensae-prog23-1/input/", budget=B):

    liste_camions = utiliteprix(x,y,data_path)
    n = len(liste_camions)

    couts = 0
    profits = 0
    p = 0
    while p != n:
        profit, prix, k = liste_camions[p]
        bc = budget-couts
        if prix <= bc:
            couts += prix
            profits += profit
            liste_camions[p][2] = 1
        p += 1
    return liste_camions, profits, couts

def aux_opti(liste_camions, budget=B):

    n = len(liste_camions)
    bij = bijection(n)

    couts = 0
    profits = 0
    cpt = 0
    p = 0
    while cpt < n:
        p = bij[cpt]
        profit, prix, k = liste_camions[p]
        bc = budget-couts
        if prix <= bc and k == 0:
            couts += prix
            profits += profit
            liste_camions[p][2] = 1
        cpt += 1
    return liste_camions, profits, couts

opti(2,2,10,B,data_path)