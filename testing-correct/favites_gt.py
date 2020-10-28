import graph_tool as gt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, type=str, help='Edges filename')
parser.add_argument('-o', '--output', required=True, type=str, help='Graph name')
args = parser.parse_args()

edges = args.input
output = args.output

f = open(edges, 'r')
g = gt.Graph(directed=True)

for line in f:
    u,v = line.split('\t')
    u = int(u)
    v = int(v)
    g.add_edge(u,v)
    g.add_edge(v,u)

g.save(output)

