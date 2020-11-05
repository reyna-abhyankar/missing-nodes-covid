'''
Converts a directory with FAVITES transmission network files into cascades
This is primarily for benchmarking.
'''

from gzip import open as gopen
from transmission_to_cascade import favites_to_cascade
import pickle as pkl
import graph_tool as gt
import argparse
import os
import time

def get_num_nodes(path):
    # maybe put method in contacts files and then pass here?
    return 100000

def main(dir_path, output_dir, fractions):
    script_dir = os.path.dirname(__file__)

    try: 
        os.mkdir(output_dir)    # create directory for graphs
    except OSError: 
        assert False, "Creation of new folder failed"

    output_folder = os.path.join(script_dir, output_dir)
    print(fractions)
    fractions_list = [float(fraction) for fraction in fractions.split(',')]
    print(fractions_list)
    # iterate over files in contacts folder
    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        num_nodes = get_num_nodes(path)
        if f.lower().endswith('.gz'):
            cascade = gopen(path)
        elif f.lower().endswith('.txt'):
            cascade = open(path)
        else:
            continue

        # Iterate over all observed fractions we want to generate pkl files for
        for fraction in fractions_list:
            if fraction < 0.1 or fraction > 0.9: continue

            pkl_dump = favites_to_cascade(cascade, num_nodes, fraction)
            new_filename = '%s_%0.1f.pkl' % (f, fraction)
            with open(os.path.join(output_folder, new_filename), 'wb') as pkl_file:
                pkl.dump(pkl_dump, pkl_file) # dump to pkl file format required by tool
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--input_directory', required=True, type=str, help="Name of FAVITES transmissions folder")
    parser.add_argument('-f', '--obs_fractions', required=True, type=str, help="Comma-separated input for which observed fractions are desired")
    parser.add_argument('-o', '--output_directory', required=True, type=str, help="Name of new output directory for cascades (.pkl)")
    args,unknown = parser.parse_known_args()
    main(args.input_directory, args.output_directory, args.obs_fractions)
    
