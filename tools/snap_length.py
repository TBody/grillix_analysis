#!/usr/bin/env python
import numpy as np
from netCDF4 import Dataset

def add_bool_arg(parser, name, default=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true')
    group.add_argument('--no_' + name, dest=name, action='store_false')
    parser.set_defaults(**{name:default})

def process_command_line_args():
    # Basic command-line interface for static-2D plotting
    import argparse

    parser = argparse.ArgumentParser(description='Check how many snaps in a snap file')

    parser.add_argument("-f", "--filepath",
                        default=None,
                        type=str,
                        required=True,
                        help="Full filepath to top-level run directory"
                        )
    
    add_bool_arg(parser, 'plot', default=False)
    add_bool_arg(parser, 'set_trace', default=False)

    args = parser.parse_args()

    return args

if __name__=="__main__":
    import os
    from os.path import join, exists
    
    args = process_command_line_args()
    filepath = args.filepath
    
    # Automatically prepend filepath to filename
    fullpath = lambda file: join(filepath, file)
    # Check if a file exists in the directory
    file_exists = lambda file: exists(fullpath(file))
    
    # Open snaps00000.nc to find the current length of snaps
    assert(file_exists("snaps00000.nc"))
    
    snapfile = Dataset(fullpath("snaps00000.nc"))
    if args.set_trace:
        import ipdb; ipdb.set_trace()
    print(f"Length of {filepath} is {snapfile.nsnaps_last} (tau={snapfile['tau'][-1]:10.6g})")
    if args.plot:
        import matplotlib.pyplot as plt
        plt.plot(snapfile['tau'])
        plt.xlabel("Snap number")
        plt.ylabel("Tau")
        plt.show()
    
    