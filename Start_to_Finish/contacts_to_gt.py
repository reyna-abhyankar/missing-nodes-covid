'''
Converts a FAVITES contact network into a graph tool object
'''

from gzip import open as gopen
import graph_tool as gt
import argparse

def favites_to_gt(contacts):
    # parse contact network
    g = gt.Graph(directed=True)
    for line in contacts:
        if isinstance(line,bytes): 
            l = line.decode().strip()
        else: 
            l = line.strip()
        
        if len(l) == 0 or l[0] == '#': 
            continue
        assert l.startswith('NODE\t') or l.startswith('EDGE\t'), "Contact network is not in the FAVITES format"
        if l.startswith('NODE\t'): 
            continue

        try: 
            n,u,v,a,d = l.split()
            u = int(u)
            v = int(v)
        except: 
            assert False, "Contact network is not in the FAVITES format"

        # add to graph
        g.add_edge(u,v)
        g.add_edge(v,u)
    return g

def main(contacts, output):
    if contacts.lower().endswith('.gz'):
        contacts = gopen(contacts)
    else:
        contacts = open(contacts)

    if output.endswith('.gt'):
        favites_to_gt(contacts).save(output)
    else:
        favites_to_gt(contacts).save(output+'.gt')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--contact_network', required=True, type=str, help="FAVITES contact network")
    parser.add_argument('-o', '--output_filename', required=True, type=str, help="Output filename (.gt)")
    args,unknown = parser.parse_known_args()
    main(args.contact_network, args.output_filename)
