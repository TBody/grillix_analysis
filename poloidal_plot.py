#!/usr/bin/env python
# Import CLI user interface
from source.interface.CLI import (
    BaseCLI,
    FilepathArg, SaveFilepathArg,
    GroupArg, TitleArg,
    TimeSliceArg, ToroidalSliceArg,
    AllReductionArg,
    SI_unitsArg, LogScaleArg, ErrorSnapsArg
)

# Set up command-line interface
from source.measurements.Variable import variable_groups
class PoloidalPlotCLI(BaseCLI):

    def __init__(self, parse=False, display=False):
        super().__init__("plot values over a poloidal plane")
        
        self.filepath           = FilepathArg(self)
        self.save               = SaveFilepathArg(self)
        self.group              = GroupArg(self, variable_groups.keys(), default="BaseVariable")
        self.title              = TitleArg(self)
        self.time_slice         = TimeSliceArg(self)
        self.toroidal_slice     = ToroidalSliceArg(self)
        self.allred             = AllReductionArg(self)
        self.convert_to_si      = SI_unitsArg(self)
        self.log_scale          = LogScaleArg(self)
        self.error_snaps        = ErrorSnapsArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source
from source.run import Run
from source.measurements.Projector import Poloidal
from ipdb import launch_ipdb_on_exception
import source.canvas as canvas

if __name__=="__main__":
    # Wrapping everything with "with launch_ipdb_on_exception():" has the helpful effect that, upon a crash, the ipdb debugger is launched
    # so you can find out what went wrong
    with launch_ipdb_on_exception():
        # CLI behaves exactly like a dictionary. If you want, you can modify it with standard dictionary methods, or replace it altogether
        CLI = PoloidalPlotCLI(parse=True, display=True)
        
        filepath = CLI['filepath']
        use_error_snaps = CLI['error_snaps']
        group = CLI['group']
        allreduce = CLI['allreduce']

        # Check the run directory and initialise the following
        # directory     = resolved paths to required files
        # parameters    = dictionary of parameters from params.in
        # equi_type     = string giving the type of equilibrium
        # equilibrium   = interface to equilibrium variables
        # normalisation = dimensional quantities which give conversion to SI
        # grid          = vgrid + perpghost, including vector_to_matrix routines
        # 
        run = Run(filepath, use_error_snaps=use_error_snaps)

        # Select a list of Variable types to plot
        variables = variable_groups[group]

        # Construct the list of operators
        operators = []
        
        # Request the 'Poloidal' projector. A projector takes z(t, phi, l) and maps it to a 2D array, in this case z(x, y)
        # The treatment of the 't' and 'phi' axis is via an AllReduction operator, passed as the reduction keyword
        projector = Poloidal(reduction=allreduce)

        figure = canvas.subplots_with_title(naxs=len(variables), title="Test")

        from ipdb import set_trace; set_trace()
        figure.axes[0][0]


        figure.show()

        # # Generate a figure which has enough subplots to plot all the variables, and request a figure title, conversion to
        # # SI and logarithmic plot depending on ctrl arguments
        # figure = Plot(run                 = run,
        #               naxs                = len(variables),
        #               title               = ctrl["title"],
        #               convert             = ctrl["convert_to_SI"],
        #               log_scale = ctrl["log_scale"])

        # # For each Subplot in the Plot, set values for the run, projector, variable, and operators
        # figure.set_data_array(run=run, projector=projector, variables=variables, operators=operators)

        # # For each Subplot in the Plot, fill the axes with values
        # figure.fill_values(time_slice=ctrl["time_slice"], toroidal_slice=ctrl["toroidal_slice"])

        # # Save or display the figure
        # if ctrl["save"]:
        #     figure.save_as_png(ctrl["save"])
        # else:
        #     figure.show()