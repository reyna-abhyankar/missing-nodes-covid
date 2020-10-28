import graph_tool as gt

def int_conv(n):
    lead = n.find('-', 8)
    num = int(n[8:lead])*10000
    num += int(n[lead+1:])
    return num

f = open('edges.txt', 'r')
g = gt.Graph(directed=True)

for line in f:
    u,v = line.split('\t')
    u = int_conv(u)
    v = int_conv(v)
    g.add_edge(u,v)
    g.add_edge(v,u)

g.save('favites.gt')

