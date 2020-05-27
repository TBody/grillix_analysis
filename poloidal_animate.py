#!/usr/bin/env python
# Import CLI user interface
from source.interface import (
    BaseCLI,
    FilepathArg, SaveFilepathArg,
    GroupArg, TitleArg,
    TimeSliceArg, ToroidalSliceArg,
    ReductionArg,
    SI_unitsArg, LogScaleArg, ErrorSnapsArg, ExcludeOutliersArg
)

# Set up command-line interface
from source.measurements.Variable.variable_groups import variable_groups
class PoloidalAnimateCLI(BaseCLI):

    def __init__(self, parse=False, display=False):
        super().__init__("animate values over a poloidal plane")
        
        self.filepath           = FilepathArg(self)
        self.save               = SaveFilepathArg(self)
        self.group              = GroupArg(self, variable_groups.keys(), default="BaseVariable")
        self.title              = TitleArg(self)
        self.time_slice         = TimeSliceArg(self, default_all=True, allow_range=True, allow_step=True)
        self.toroidal_slice     = ToroidalSliceArg(self)
        self.reduction          = ReductionArg(self)
        self.SI_units           = SI_unitsArg(self)
        self.exclude_outliers   = ExcludeOutliersArg(self)
        self.log_scale          = LogScaleArg(self)
        self.error_snaps        = ErrorSnapsArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source
from source import usrenv
from source.run import Run
from source.measurements.Projector import Poloidal
from source.measurements import Measurement, measurement_array_from_variable_array
from ipdb import launch_ipdb_on_exception
from source.canvas import Canvas
from source.canvas.Painter import PoloidalPlot
from source.shared import check_ffmpeg

if __name__=="__main__":
    # Wrapping everything with "with launch_ipdb_on_exception():" has the helpful effect that, upon a crash, the ipdb debugger is launched
    # so you can find out what went wrong
    with launch_ipdb_on_exception():
        # CLI behaves exactly like a dictionary. If you want, you can modify it with standard dictionary methods, or replace it altogether
        CLI = PoloidalAnimateCLI(parse=True, display=True)
        
        filepath         = CLI['filepath']
        use_error_snaps  = CLI['error_snaps']
        group            = CLI['group']
        reduction        = CLI['reduction']
        title            = CLI['title']
        SI_units         = CLI['SI_units']
        exclude_outliers = CLI['exclude_outliers']
        log_scale        = CLI['log_scale']
        save_path        = CLI['save']

        time_slice       = CLI['time_slice']
        toroidal_slice   = CLI['toroidal_slice']

        if save_path:
            check_ffmpeg()

        # Check the run directory and initialise the following
        # directory     = resolved paths to required files
        # parameters    = dictionary of parameters from params.in
        # equi_type     = string giving the type of equilibrium
        # equilibrium   = interface to equilibrium variables
        # normalisation = dimensional quantities which give conversion to SI
        # grid          = vgrid + perpghost, including vector_to_matrix routines
        # 
        run = Run(filepath)
        run.directory.use_error_snaps = use_error_snaps

        # Select a list of Variable types to plot
        variables = variable_groups[group]

        # Construct the list of operators
        operators = []
        
        # Request the 'Poloidal' projector. A projector takes z(t, phi, l) and maps it to a 2D array, in this case z(x, y)
        # The treatment of the 't' and 'phi' axis is via an AllReduction operator, passed as the reduction keyword
        projector = Poloidal()
        
        # Bundle the projector, variable, reduction and operators together into a "measurement" object
        # Make one measurement for each variable in variables
        measurement_array = measurement_array_from_variable_array(projector=projector,
                                                                  variable_array=variables,
                                                                  reduction=reduction,
                                                                  operators=operators,
                                                                  run=run)

        # Make a clean figure
        canvas = Canvas()

        # Make a subplot for each measurement in measurement_array
        # Associate a "Painter" (which takes a measurement and draws its values)
        # A "Colorbar" for each "Painter" will be automatically generated
        canvas.subplots_from_measurement_array(
            painter=PoloidalPlot,
            measurement_array=measurement_array,
            run=run,
            SI_units=SI_units,
            log_scale=log_scale,
            exclude_outliers=exclude_outliers)

        # Add a title
        canvas.title(title_string=title, SI_units=SI_units, run=run)
        
        ######################################################################
        # Up until this point, everything has been identical to making a static plot. Now, we need to
        # do a few animation-specific things. These are all wrapped in "make_animator"
        canvas.make_animator(run=run, time_slice=time_slice, toroidal_slice=toroidal_slice)

        # # Save or display the canvas
        if save_path:
            canvas.save_animation(save_path)
        else:
            canvas.show()