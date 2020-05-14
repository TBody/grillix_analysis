#!/usr/bin/env python
# Import CLI user interface
from source.UserInterface.CLI import (
    BaseCLI,
    FilepathArg, SaveFilepathArg, SnapNameArg,
    GroupArg, TitleArg,
    TimeSliceArg, ToroidalSliceArg,
    AllReductionArg,
    ConvertToSIArg, DisplayLogarithmArg
)

# Set up command-line interface
from source.Variable import variable_groups
class PoloidalAnimateCLI(BaseCLI):

    def __init__(self, parse=False, display=False):
        super().__init__("Animate values over a poloidal plane")
        
        self.filepath           = FilepathArg(self)
        self.save               = SaveFilepathArg(self)
        self.snap_name          = SnapNameArg(self)
        self.group              = GroupArg(self, variable_groups.keys(), default="BaseVariable")
        self.title              = TitleArg(self)
        self.time_slice         = TimeSliceArg(self, default_all=True, allow_range=True, allow_step=True)
        self.toroidal_slice     = ToroidalSliceArg(self)
        self.allred             = AllReductionArg(self)
        self.convert_to_si      = ConvertToSIArg(self)
        self.display_logarithm  = DisplayLogarithmArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source
from source.Run import Run
from source.Display import Animate
from source.Projector.Poloidal import Poloidal
from ipdb import launch_ipdb_on_exception
from source.shared import check_ffmpeg

if __name__=="__main__":
    # Wrapping everything with "with launch_ipdb_on_exception():" has the helpful effect that, upon a crash, the ipdb debugger is launched
    # so you can find out what went wrong
    with launch_ipdb_on_exception():
        check_ffmpeg()
        # CLI behaves exactly like a dictionary. If you want, you can modify it with standard dictionary methods, or replace it altogether
        CLI = PoloidalAnimateCLI(parse=True, display=True)
        
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

        # Select a list of Variable types to animate
        variables = variable_groups[ctrl["group"]]

        # Construct the list of operators
        operators = []
        
        # Request the 'Poloidal' projector. A projector takes z(t, phi, l) and maps it to a 2D array, in this case z(x, y)
        # The treatment of the 't' and 'phi' axis is via an AllReduction operator, passed as the reduction keyword
        projector = Poloidal(reduction=ctrl["allreduce"])

        # Generate a figure which has enough subplots to animate all the variables, and request a figure title, conversion to
        # SI and logarithmic plt depending on ctrl arguments
        figure = Animate(run                 = run,
                         naxs                = len(variables),
                         title               = ctrl["title"],
                         convert             = ctrl["convert_to_SI"],
                         display_logarithmic = ctrl["display_log"])

        # For each Subplot in figure, set values for the run, projector, variable, and operators
        figure.set_data_array(run=run, projector=projector, variables=variables, operators=operators)

        # For each Subplot in figure, animate the values
        figure.setup_animation(time_slice=ctrl["time_slice"], toroidal_slice=ctrl["toroidal_slice"])

        # Save the animation, or animate it on repeat
        if ctrl["save"]:
            figure.save_animation(ctrl["save"])
        else:
            figure.animate_on_repeat()