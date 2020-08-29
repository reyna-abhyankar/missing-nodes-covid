import sys
import networkx as nx
from graph_tool import load_graph

filename = 'graph_weighted_0.5.gt'
if len(sys.argv)>1:
    filename = sys.argv[1]

g = load_graph(filename)
n = nx.MultiDiGraph() # directed graphs with self loops and parallel edges

edges = []
for e in g.edges():
    edges.append([e.source(), e.target()])

n.add_edges_from(edges)

nx.write_gexf(n, 'infectious.gexf')