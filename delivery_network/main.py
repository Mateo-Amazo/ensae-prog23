from graph import Graph, graph_from_file
import numpy as np
import matplotlib.pyplot as plt

data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)
g.connected_components()

x=[1,3,5,7]
y=[2,4,6,1]
plt.plot(x,y)

x = [5,6,7]
y = [8,9,10]
plt.plot(x,y,color = 'red')
plt.show()











































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