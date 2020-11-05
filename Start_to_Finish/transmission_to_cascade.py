from gzip import open as gopen
import pickle as pkl
import random
import numpy as np
import math
import graph_tool as gt 
import argparse
import os

def favites_to_cascade(cascade, cascade_array, OBS_FRAC):
    # parse transmission network
    true_edges = []
    infected = []

    for line in cascade:
        if isinstance(line,bytes): 
            l = line.decode().strip()
        else: 
            l = line.strip()
        
        try:
            u,v,t = line.split()
            v = int(v)
            t = float(t)
            cascade_array[v] = t
            if t > 0: 
                infected.append(v)
            if u != 'None':
                u = int(u)
                true_edges.append((u,v))
        except:
            assert False, "Transmission file is not in the FAVITES format"
    
    obs = np.asarray(random.sample(infected,math.floor(len(infected)*OBS_FRAC)))
    print("Observation Fraction: ", OBS_FRAC)

    filename = 'favites_%0.1f.pkl' % OBS_FRAC
    pkl.dump((obs, np.asarray(cascade_array), true_edges), open(filename, 'wb'))

def main(num_nodes, cascade, OBS_FRAC):
    cascade_array = [-1]*num_nodes

    if cascade.lower().endswith('.gz'):
        cascade = gopen(cascade)
    else:
        cascade = open(cascade)

    favites_to_cascade(cascade, cascade_array, OBS_FRAC)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--nodes', required=True, type=int, help='Number of nodes')
    parser.add_argument('-c', '--cascade', required=True, type=str, help='FAVITES transmission cascade file')
    parser.add_argument('-o', '--obsfrac', required=True, default=0.2, type=float, help='Fraction of observed infected to total infected')
    args,unknown = parser.parse_known_args()
    main(args.nodes, args.cascade, args.obsfrac)





