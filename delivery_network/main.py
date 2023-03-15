import sys 
sys.path.append("delivery_network/")

from graph import Graph, graph_from_file
from graph import min_power2

data_path = "input/"
file_name = "network.2.in"







































def random_graph(n,m,max_power,max_dist) : #Génère un graphe aléatoire avec n sommets et m arretes, un power maximal sur un trajet de max_power et une distance maximale sur un trajet de max_dist

    g = Graph([k for k in range(n)])

    for k in range(m) :
        
        src = rd.randint(0,n)
        dest = rd.randint(0,n)
        
        while src == dest :
            dest = rd.randint(0,n)
        
        power = rd.randint(0,max_power +1)
        dist = rd.randint(0,max_dist + 1)

        g.add_edge(src,dest,power,dist)
    
    return g