import pickle as pkl
import random
import numpy as np
import math
import graph_tool as gt 
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nodes', required=True, type=str, help='Nodes filename')
parser.add_argument('-c', '--cascade', required=True, type=str, help='Cascade filename')
parser.add_argument('-s', '--sorted', required=False, default=True, type=bool, help='True if node file is sorted')
parser.add_argument('-o', '--obsfrac', required=True, default=0.2, type=float, help='Fraction of observed infected to total infected')
args = parser.parse_args()

nodes = args.nodes
cascade = args.cascade
is_sorted = args.sorted
OBS = args.obsfrac
cascade_array = []

if is_sorted:
    with open(nodes, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
    cascade_array = [-1]*int(last_line)
else:
    f = open(nodes, 'r')
    for line in enumerate(f):
        cascade_array.append(-1)
    f.close()

true_edges = []
f = open(cascade, 'r')
for line in f:
    u,v,t = line.split('\t')
    v = int(v)
    t = float(t.rstrip('\n'))
    cascade_array[v] = t
    if u != 'None':
        u = int(u)
        true_edges.append((u,v))
f.close()

infected = []
for i,time in enumerate(cascade_array):
    if time>0: 
        infected.append(i)

obs = np.asarray(random.sample(infected,math.floor(len(infected)*OBS)))
cf = len(infected)/len(cascade_array)
print("Cascade Fraction: ", cf)
print("Observation Fraction: ", OBS)
filename = 'favites_%0.1f.pkl' % OBS
pkl.dump((obs, np.asarray(cascade_array), true_edges), open(filename, 'wb'))

