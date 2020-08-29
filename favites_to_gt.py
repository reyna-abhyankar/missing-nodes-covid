import graph_tool as gt

def int_conv(n):
    lead = n.find('-', 8)
    num = int(n[8:lead])*10000
    num += int(n[lead+1:])
    return num

f = open('edges.txt', 'r')
g = gt.Graph(directed=False)

for line in f:
    u,v = line.split('\t')
    g.add_edge(int_conv(u), int_conv(v))

g.save('favites.gt')

