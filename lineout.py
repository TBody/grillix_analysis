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

def plot_lineouts(lineouts):
    flux_surface, _ = FluxSurface(run=run)()
    plt.contour(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(flux_surface.flatten()), 100)

    for lineout in lineouts.values():
        lineout.plot_sample_line()

    plt.title(title)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.show()

def setup_results_file(results_file, run, lineouts, measurement_arrays, snap_indices, time_slice, toroidal_slice, prevent_overwrite=True):
    if prevent_overwrite: assert not(results_file.exists()), f"Error: file {results_file} already exists. Manually remove before continuing"
    
    rootgrp = Dataset(results_file, 'w')
        
    rootgrp.createDimension("points", lineout_resolution)
    rootgrp.createDimension("time", None)
    sample_times = rootgrp.createVariable("sample_times", "f8", ("time",))

    sample_times[:] = np.atleast_1d(run.tau_values[time_slice])
    rootgrp.tau_normalisation = run.normalisation.tau_0.to('s').magnitude
    rootgrp.tau_normalisation_units = "s"

    measurement_vars = {}
    # Write in header for each lineout
    for key, projector in lineouts.items():

        lineout_grp = rootgrp.createGroup(key)
        sample_x = lineout_grp.createVariable("sample_x", "f8", ("points",))
        sample_y = lineout_grp.createVariable("sample_y", "f8", ("points",))
        sample_rho = lineout_grp.createVariable("sample_rho", "f8", ("points",))
        sample_arc = lineout_grp.createVariable("sample_arc", "f8", ("points",))

        sample_x[:] = projector.x_interp
        sample_y[:] = projector.y_interp
        sample_rho[:] = projector.rho_values()
        sample_arc[:] = projector.arc_l
        lineout_grp.spatial_factor = run.normalisation.R0.magnitude
        lineout_grp.spatial_factor_units = str(run.normalisation.R0.units)

        measurement_vars[key] = np.empty((len(measurement_arrays[key])), dtype=NCVariable)

        for measurement_id in range(len(measurement_arrays[key])):
            variable_reference = measurement_arrays[key][measurement_id].variable.title
            variable_reference = variable_reference.replace(" ", "_").replace(".", "")

            var_grp = lineout_grp.createGroup(variable_reference)
            var_grp.createVariable("values", "f8", ("time", "points"))

            normalisation_factor = measurement_arrays[key][measurement_id].variable.normalisation_factor
            var_grp.normalisation_factor = normalisation_factor.magnitude
            var_grp.normalisation_factor_units = str(normalisation_factor.units)

            measurement_vars[key][measurement_id] = var_grp
    
    return measurement_vars

def inner_loop(snap_indices, measurement, toroidal_slice):
    results = np.zeros((len(snap_indices), lineout_resolution))

    for t, time in zip(range(len(snap_indices)), snap_indices):
        print(f"\tExtracting data at {time} of [{snap_indices[0]}-{snap_indices[-1]}] for {key}, {measurement.variable.title}")

        results[t, :], _ = measurement(time_slice=[time], toroidal_slice=toroidal_slice)
    
    return results

def fill_values(lineouts, measurement_arrays, measurement_vars, snap_indices, toroidal_slice):

    for key, projector in lineouts.items():

        for measurement, measurement_id in zip(measurement_arrays[key], range(len(measurement_arrays[key]))):
            
            var_grp = measurement_vars[key][measurement_id]
            
            results = inner_loop(snap_indices, measurement, toroidal_slice)
            
            var_grp["values"][:, :] = results

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
        lineouts = {
            # "OMP": Lineout("OMP", resolution=lineout_resolution),
            # "IMP": Lineout("IMP", resolution=lineout_resolution),
            "MP": Lineout("MP", resolution=lineout_resolution),
            # "VMP": Lineout("VMP", resolution=lineout_resolution),
            "LFS_C0": Lineout("LFS_C0", resolution=lineout_resolution),
            # "LFS_TARGET": Lineout("LFS_TARGET", resolution=lineout_resolution),
            "HFS_C0": Lineout("HFS_C0", resolution=lineout_resolution),
            # "HFS_TARGET": Lineout("HFS_TARGET", resolution=lineout_resolution),
            # "AX": Lineout("AX", resolution=lineout_resolution),
            "AXPX": Lineout("AXPX", resolution=lineout_resolution)
            # "AXP0": Lineout("AXP0", resolution=lineout_resolution),
        }

        measurement_arrays = {}
        print("Initialising measurement arrays")
        for key, projector in lineouts.items():

            measurement_arrays[key] = measurement_array_from_variable_array(
                projector=projector,
                variable_array=variables,
                reduction=reduction,
                operators=operators,
                run=run)
        
        # plot_lineouts(lineouts)
        
        snap_indices = run.snap_indices[time_slice]

        results_file = Path(filepath)/f"lineouts_{group}_{snap_indices[0]}_{snap_indices[1]}.nc"
        
        if not results_file.exists():
            print(f"File {results_file} doesn't exist. Making file now.")

            print("Setting up results file")
            measurement_vars = setup_results_file(
                results_file, run, lineouts, measurement_arrays, snap_indices, time_slice, toroidal_slice, prevent_overwrite=False)

            print("Filling results file")
            fill_values(lineouts, measurement_arrays, measurement_vars, snap_indices, toroidal_slice)

        # rootgrp = Dataset(results_file, 'r')

        # plt.pcolormesh(rootgrp["MP"]["sample_rho"][np.logical_not(np.isnan(rootgrp["MP"]["sample_rho"]))],
        #                rootgrp["sample_times"], 
        #                rootgrp["MP"]["Density"]["values"][:,np.logical_not(np.isnan(rootgrp["MP"]["sample_rho"]))]
        #                )

        # plt.show()


