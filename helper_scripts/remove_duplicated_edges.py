import sys
import graph_tool
from graph_tool import load_graph

g = load_graph(sys.argv[1])

set_list = [set(a) for a in g.edges()] # collect all edges, lose positional information
remove_list = [] # initialise

for i in range(len(set_list)):
    edge = set_list.pop(0) # look at zeroth element in list:

    # if there is still an edge like the current one in the list, 
    # add the current edge to the remove list:
    if set_list.count(edge) > 0:
        u,v = edge 

        # add the reversed edge
        remove_list.append((v, u))

        # alternatively, add the original edge: 
        # remove_list.append((u, v))

for edge in remove_list:
    g.remove_edge(edge)

print(g.num_vertices())
print(g.num_edges())

#g.save("graph_weighted_0.5.gt")
