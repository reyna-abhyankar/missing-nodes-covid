'''
Converts a directory with FAVITES contact network files into respective graph tool objects
'''

from gzip import open as gopen
from file_to_gt import favites_to_gt
import graph_tool as gt
import argparse
import os
import time
    
if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--path', required=True, type=str, help="Path to FAVITES contact networks")
    parser.add_argument('-o', '--output_directory', required=True, type=str, help="Name of new output directory for graphs (.gt)")
    args,unknown = parser.parse_known_args()
    dir_path = args.path
    output_dir = args.output_directory

    script_dir = os.path.dirname(__file__)

    try: 
        os.mkdir(output_dir)
    except OSError: 
        assert False, "Creation of new folder failed"

    output_folder = os.path.join(script_dir, output_dir)

    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        if f.lower().endswith('.gz'):
            contacts = gopen(path)
        elif f.lower().endswith('.txt'):
            contacts = open(path)
        else:
            continue

        g = favites_to_gt(contacts)
        new_filename = f+'.gt'
        g.save(os.path.join(output_folder, new_filename))

    end = time.time()
    print(end - start)
        

        
    
