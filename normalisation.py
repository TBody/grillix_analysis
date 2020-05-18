#!/usr/bin/env python
# Import CLI user interface
from source.UserInterface.CLI import (
    BaseCLI,
    FilepathArg,
    LaunchIPDBArg
)

# Set up command-line interface
from source.Variable import variable_groups
class NormalisationCLI(BaseCLI):

    def __init__(self, parse=False, display=False):
        super().__init__("return normalisation values")
        
        self.filepath           = FilepathArg(self)
        self.launch_ipdb        = LaunchIPDBArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source, as well as numpy in case you want to
# do dimensional calculations
from source import np
from source.Run import Run
from ipdb import launch_ipdb_on_exception

if __name__=="__main__":
    # Wrapping everything with "with launch_ipdb_on_exception():" has the helpful effect that, upon a crash, the ipdb debugger is launched
    # so you can find out what went wrong
    with launch_ipdb_on_exception():
        # CLI behaves exactly like a dictionary. If you want, you can modify it with standard dictionary methods, or replace it altogether
        CLI = NormalisationCLI(parse=True, display=True)
        
        # Extract the dictionary -- this could equally be determined programmatically
        # We call it 'ctrl' for control, but it doesn't really matter: it is just a normal dictionary
        ctrl = CLI.dict

        # Check the run directory and initialise the following
        # directory     = resolved paths to required files
        # parameters    = dictionary of parameters from params.in
        # equi_type     = string giving the type of equilibrium
        # equilibrium   = interface to equilibrium variables
        # normalisation = dimensional quantities which give conversion to SI
        # grid          = vgrid + perpghost, including vector_to_matrix routines
        # 
        run = Run(ctrl['filepath'])

        # Just want to return the normalisation parameters
        N = run.normalisation

        print(N)

        if ctrl["launch_ipdb"]:
            run.convert = True
            import ipdb
            ipdb.set_trace()
            print("Launching ipdb -- you can use the workspace interactively")