#!/usr/bin/env python
# Import CLI user interface
from source.interface import (
    BaseCLI,
    FilepathArg, SaveFilepathArg,
    GroupArg, TitleArg,
    TimeSliceArg, ToroidalSliceArg,
    ReductionArg,
    SI_unitsArg, LogScaleArg
)

# Set up command-line interface
from source.measurements.measurement_groups import measurement_groups
class LineoutCLI(BaseCLI):

    def __init__(self, parse=False, display=False):
        super().__init__("plot values over a poloidal plane")

        self.filepath           = FilepathArg(self)
        self.save               = SaveFilepathArg(self)
        self.group              = GroupArg(self, measurement_groups.keys(), default="BaseVariable")
        self.title              = TitleArg(self)
        self.time_slice         = TimeSliceArg(self)
        self.toroidal_slice     = ToroidalSliceArg(self)
        self.reduction          = ReductionArg(self)
        self.SI_units           = SI_unitsArg(self)
        self.log_scale          = LogScaleArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source
from source import plt, np, Dataset, Path
from netCDF4 import Variable as NCVariable
from source.run import Run
from source.measurements import Measurement, measurement_array_from_variable_array
from source.measurements.Projector import Lineout
from source.measurements.Variable.StaticVariable import FluxSurface
from pathos.multiprocessing import ProcessingPool as Pool

from ipdb import launch_ipdb_on_exception

lineout_resolution = 100

def plot_projector(projector):
    flux_surface, _ = FluxSurface(run=run)()
    plt.contour(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(flux_surface.flatten()), 100)

    projector.plot_interps()

    plt.title(title)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.show()

def setup_results_file(results_file, run, projector, measurement_array, snap_indices, time_slice, toroidal_slice, prevent_overwrite=True):
    if prevent_overwrite: assert not(results_file.exists()), f"Error: file {results_file} already exists. Manually remove before continuing"
    
    flux_surface, _ = FluxSurface(run=run)()
    flux_surface = run.grid.vector_to_matrix(flux_surface.flatten())
    rootgrp = Dataset(results_file, 'w')
        
    rootgrp.createDimension("time", None)
    sample_times = rootgrp.createVariable("sample_times", "f8", ("time",))

    sample_times[:] = np.atleast_1d(run.tau_values[time_slice])
    rootgrp.tau_normalisation = run.normalisation.tau_0.to('s').magnitude
    rootgrp.tau_normalisation_units = "s"

    measurement_vars = []

    for measurement_id in range(len(measurement_array)):
        variable_reference = measurement_array[measurement_id].variable.title
        variable_reference = variable_reference.replace(" ", "_").replace(".", "")

        var_grp = rootgrp.createGroup(variable_reference)

        normalisation_factor = measurement_array[measurement_id].variable.normalisation_factor
        var_grp.normalisation_factor = normalisation_factor.magnitude
        var_grp.normalisation_factor_units = str(normalisation_factor.units)

        lineout_vars = {}

        # Write in header for each lineout
        for key, interp in projector.interps.items():

            lineout_grp = var_grp.createGroup(key)
            lineout_grp.createDimension("points", interp.x_interp.size)
            sample_x = lineout_grp.createVariable("sample_x", "f8", ("points",))
            sample_y = lineout_grp.createVariable("sample_y", "f8", ("points",))
            sample_rho = lineout_grp.createVariable("sample_rho", "f8", ("points",))
            sample_arc = lineout_grp.createVariable("sample_arc", "f8", ("points",))

            val_var = lineout_grp.createVariable("values", "f8", ("time", "points"))

            sample_x[:] = interp.x_interp
            sample_y[:] = interp.y_interp
            sample_rho[:] = interp.rho_values(flux_surface)
            sample_arc[:] = interp.arc_l
            lineout_grp.spatial_factor = run.normalisation.R0.magnitude
            lineout_grp.spatial_factor_units = str(run.normalisation.R0.units)

            lineout_vars[key] = val_var
        
        measurement_vars.append(lineout_vars)

    return measurement_vars

def fill_values(projector, measurement_array, measurement_vars, snap_indices, toroidal_slice):

    results = {}
    for measurement, measurement_id in zip(measurement_array, range(len(measurement_array))):
        for key, lineout in projector.interps.items():
            results[key] = np.zeros((len(snap_indices), lineout.x_interp.size))


        for t, time in zip(range(len(snap_indices)), snap_indices):

            print(f"\tExtracting data at {time} of [{snap_indices[0]}-{snap_indices[-1]}], {measurement.variable.title}")

            results_at_time, _ = measurement(time_slice=[time], toroidal_slice=toroidal_slice)
            
            for key in projector.interps.keys():
                results[key][t, :] = results_at_time[key]

        for key in projector.interps.keys():
            var_grp = measurement_vars[measurement_id][key]
            var_grp[:, :] = results[key]

if __name__=="__main__":
    # Wrapping everything with "with launch_ipdb_on_exception():" has the helpful effect that, upon a crash, the ipdb debugger is launched
    # so you can find out what went wrong
    with launch_ipdb_on_exception():
        # CLI behaves exactly like a dictionary. If you want, you can modify it with standard dictionary methods, or replace it altogether
        CLI = LineoutCLI(parse=True, display=False)

        filepath         = CLI['filepath']
        group            = CLI['group']
        reduction        = CLI['reduction']
        title            = CLI['title']
        SI_units         = CLI['SI_units']
        log_scale        = CLI['log_scale']
        save_path        = CLI['save']

        time_slice       = CLI['time_slice']
        toroidal_slice   = CLI['toroidal_slice']

        run = Run(filepath)

        # Select a list of Variable types to plot
        variables = measurement_groups[group]

        # Construct the list of operators
        operators = []

        # Request the different projectors
        projector = Lineout(resolution = lineout_resolution)

        measurement_array = measurement_array_from_variable_array(
                                projector=projector,
                                variable_array=variables,
                                reduction=reduction,
                                operators=operators,
                                run=run)
        
        # plot_projector(projector)
        # quit()
        
        snap_indices = run.snap_indices[time_slice]

        results_file = Path(filepath)/f"projector_{group}_{snap_indices[0]}_{snap_indices[-1]}.nc"
        
        if not results_file.exists():
            print(f"File {results_file} doesn't exist. Making file now.")

            print("Setting up results file")
            measurement_vars = setup_results_file(
                results_file, run, projector, measurement_array, snap_indices, time_slice, toroidal_slice, prevent_overwrite=False)

            print("Filling results file")
            fill_values(projector, measurement_array, measurement_vars, snap_indices, toroidal_slice)

        else:
            print(f"File {results_file} exists. Reading from file.")
            rootgrp = Dataset(results_file, 'r')

            # plt.pcolormesh(rootgrp["Density"]["OMP"]["sample_rho"],
            #             rootgrp["sample_times"],
            #             rootgrp["Density"]["OMP"]["values"]
            #             )

            plt.show()


