import pickle as pkl
import random
import numpy as np
import math
import graph_tool as gt 

f = open('nodes.txt', 'r')
inf_dict = {}
for i,line in enumerate(f):
    inf_dict[line.strip('\n')] = [-1, i]
f.close()

true_edges = []
f = open('cascade.txt', 'r')
for line in f:
    u,v,t = line.split('\t')
    t = float(t.rstrip('\n'))
    inf_dict[v][0] = t
    if u != 'None':
        u_i = inf_dict[u][1]
        v_i = inf_dict[v][1]
        true_edges.append((u_i,v_i))
f.close()

cascade = [arr[0] for arr in list(inf_dict.values())]
infected = []
for i in range(len(cascade)):
    if cascade[i]>=0: infected.append(i)

obs = np.asarray(random.sample(infected,math.floor(len(infected)/5)))

pkl.dump((obs, np.asarray(cascade), true_edges), open('favites.pkl', 'wb'))
