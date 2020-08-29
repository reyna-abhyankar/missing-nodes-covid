import pickle
import random
import numpy as np
import math
import graph_tool as gt 
from collections import OrderedDict

f = open('nodes.txt', 'r')

inf_dict = {}
for line in f:
    inf_dict[line] = -1

f = open('cascade.txt', 'r')

for line in f:
    n,d = line.split('\t')
    d = float(d.rstrip('\n'))
    inf_dict[n] = d

cascade = list(inf_dict.values())
infected = []
for i in range(len(cascade)):
    if cascade[i]>0: infected.append(i)

print(len(infected))
obs = np.asarray(random.sample(infected,math.floor(len(infected)/5)))
print(len(obs))

#pickle.dump((obs, cascade), open('favites.pkl', 'wb'))
