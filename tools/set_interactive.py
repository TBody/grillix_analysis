#!/usr/bin/env python

def add_bool_arg(parser, name, default=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true')
    group.add_argument('--no_' + name, dest=name, action='store_false')
    parser.set_defaults(**{name:default})

def process_command_line_args():
    # Basic command-line interface for static-2D plotting
    import argparse

    parser = argparse.ArgumentParser(description='Add/remove a file which sets whether to run with a GUI')
    
    add_bool_arg(parser, 'yes', default=False)
    add_bool_arg(parser, 'no', default=False)

    args = parser.parse_args()

    return args

if __name__=="__main__":
    from pathlib import Path
    import os

    args = process_command_line_args()
    
    if args.yes and args.no:
        raise RuntimeError(f"CLI error. Set only one flag")

    if not(args.yes or args.no):
        raise RuntimeError(f"CLI error. Set --yes (run with GUI) or --no (run without GUI)")
        
    flag_file = Path(__file__).absolute().parents[1] / "no.interactive"
    print(f"flag file is {flag_file}. Exists: {flag_file.exists()}")

    if args.yes and flag_file.exists():
        print("Removing flag file")
        os.remove(flag_file)
    
    if args.no and not(flag_file.exists()):
        print("Making flag file")
        flag_file.touch()
        