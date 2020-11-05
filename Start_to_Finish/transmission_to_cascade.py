'''
Converts a FAVITES transmission network into a cascade
that can be used by the cascade reconstruction tool
'''

from gzip import open as gopen
import pickle as pkl
import random
import numpy as np
import math
import graph_tool as gt 
import argparse
import os

def favites_to_cascade(cascade, num_nodes, OBS_FRAC):
    # parse transmission network
    cascade_array = [-1]*num_nodes      
        # measure infection times: -1 = uninfected, 0 = seed, etc.
    true_edges = []     # represents all transmissions
    infected = []       # represents all infected nodes

    for line in cascade:
        if isinstance(line,bytes): 
            l = line.decode().strip()
        else: 
            l = line.strip()
        
        try:
            u,v,t = l.split()
            v = int(v)
            t = float(t)
            cascade_array[v] = t

            # add to edges
            if u != 'None':
                u = int(u)
                true_edges.append((u,v))
            infected.append(v)      
                # for favites, we are guaranteed that every node is only infected once
                # might not hold for all input
        except:
            assert False, "Transmission file is not in the FAVITES format"
    
    # Take a random fraction (OBS_FRAC) of the infected nodes and put them in an array
    obs = np.asarray(random.sample(infected,math.floor(len(infected)*OBS_FRAC)))
    return (obs, np.asarray(cascade_array), true_edges)
    

def main(num_nodes, cascade, OBS_FRAC, fileprefix):
    if cascade.lower().endswith('.gz'):
        cascade = gopen(cascade)
    else:
        cascade = open(cascade)

    pkl_dump = favites_to_cascade(cascade, num_nodes, OBS_FRAC)
    filename = '%s_%0.1f.pkl' % (fileprefix, OBS_FRAC)
    pkl.dump(pkl_dump, open(filename, 'wb')) # dump to pkl file format required by tool

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--nodes', required=True, type=int, help='Number of nodes')   # we can write code to get this too
    parser.add_argument('-c', '--cascade', required=True, type=str, help='FAVITES transmission cascade file')
    parser.add_argument('-f', '--obsfrac', required=True, type=float, help='Fraction of observed infected to total infected')
    parser.add_argument('-o', '--output_file', required=True, type=str, help='Output filename (.pkl)')
    args,unknown = parser.parse_known_args()
    main(args.nodes, args.cascade, args.obsfrac, args.output_file)





