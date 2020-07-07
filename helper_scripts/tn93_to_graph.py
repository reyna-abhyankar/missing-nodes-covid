#!/usr/bin/env python3
'''
Convert tn93 output to a NetworkX graph
'''
# parse args
from gzip import open as gopen
from sys import stdin,stdout
import networkx as nx
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input (tn93 Output CSV")
parser.add_argument('-t', '--threshold', required=False, type=float, default=float('inf'), help="Distance Threshold")
parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
args,unknown = parser.parse_known_args()
assert args.threshold >= 0, "ERROR: Length threshold must be at least 0"
if args.input == 'stdin':
    args.input = stdin
elif args.input.lower().endswith('.gz'):
    args.input = gopen(args.input)
else:
    args.input = open(args.input)
if args.output == 'stdout':
    args.output = stdout
else:
    args.output = open(args.output,'w')

# build NetworkX graph
g = nx.Graph()
for line in args.input:
    if isinstance(line,bytes):
        l = line.decode().strip()
    else:
        l = line.strip()
    if l == 'ID1,ID2,Distance':
        continue
    u,v,d = l.split(',')
    if float(d) > args.threshold:
        continue
    g.add_edge(u, v, weight=d)