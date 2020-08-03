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
        # self.save               = SaveFilepathArg(self)
        self.group              = GroupArg(self, measurement_groups.keys(), default="BaseVariable")
        self.title              = TitleArg(self)
        self.time_slice         = TimeSliceArg(self)
        self.toroidal_slice     = ToroidalSliceArg(self)
        self.reduction          = ReductionArg(self)
        # self.SI_units           = SI_unitsArg(self)
        # self.log_scale          = LogScaleArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source
from source import plt, np, Dataset, Path
from netCDF4 import Variable as NCVariable
from source.run import Run
from source.measurements import Measurement, measurement_array_from_variable_array
from source.measurements.Projector import Poloidal
from source.measurements.Variable.StaticVariable import FluxSurface, District
from source.measurements.Projector._lineout import LineInterpolator, FluxSurfaceInterpolator, PointInterpolator

from ipdb import launch_ipdb_on_exception

lineout_resolution = 100

def setup_lineouts(run):
    equi = run.equilibrium
    grid = run.grid

    district = District(run=run)
    district_array, _ = district()
    district_dict = district.inv_district_dict

    OMP = LineInterpolator(run, "OMP",
            np.linspace(1.0, grid.xmax),
            np.linspace(1.0, 1.0)*(equi.Z0 / equi.R0))
        
    IMP = LineInterpolator(run, "IMP",
            np.linspace(grid.xmin, 1.0),
            np.linspace(1.0, 1.0)*(equi.Z0 / equi.R0)        )
        
    MP = LineInterpolator(run, "MP",
            np.linspace(grid.xmin, grid.xmax),
            np.linspace(1.0, 1.0)*(equi.Z0 / equi.R0))

    VMP = LineInterpolator(run, "VMP",
            np.linspace(1.0, 1.0),
            np.linspace(equi.Z0/equi.R0, grid.ymax))
        
    LFS_C0 = LineInterpolator(run, "LFS_C0",
            run.penalisation_contours[0].x_arrays[1],
            run.penalisation_contours[0].y_arrays[1])

    LFS_TARGET = LineInterpolator(run, "LFS_TARGET",
            run.penalisation_contours[1].x_arrays[1],
            run.penalisation_contours[1].y_arrays[1])

    HFS_C0 = LineInterpolator(run, "HFS_C0",
            run.penalisation_contours[0].x_arrays[0],
            run.penalisation_contours[0].y_arrays[0])

    HFS_TARGET = LineInterpolator(run, "HFS_TARGET",
            run.penalisation_contours[1].x_arrays[0],
            run.penalisation_contours[1].y_arrays[0])
        
    AX = LineInterpolator(run, "AX",
            np.linspace(grid.xmin, grid.xmax),
            equi.point_axis(np.linspace(grid.xmin, grid.xmax), R_centre=equi.RX/equi.R0, Z_centre=equi.ZX/equi.R0))
        
    AXPX = LineInterpolator(run, "AXPX",
            np.linspace(grid.xmin, grid.xmax),
            equi.point_axis(np.linspace(grid.xmin, grid.xmax), R_centre=equi.RX/equi.R0, Z_centre=equi.ZX/equi.R0, normal=True))
        
    AXP0 = LineInterpolator(run, "AXP0",
            np.linspace(grid.xmin, grid.xmax),
            equi.point_axis(np.linspace(grid.xmin, grid.xmax), R_centre=equi.R0/equi.R0, Z_centre=equi.Z0/equi.R0, normal=True))
    
    SOL = FluxSurfaceInterpolator(run, "SOL",
            rho_level=1.01)
    
    SEP = FluxSurfaceInterpolator(run, "SEP",
            rho_level=1.00,
            in_domain=np.logical_or(
                (grid.vector_to_matrix(district_array.flatten())==district_dict["DISTRICT_CLOSED"]),
                (grid.vector_to_matrix(district_array.flatten())==district_dict["DISTRICT_SOL"]),
            ),
            closed=True
            )

    CLOSED = FluxSurfaceInterpolator(run, "CLOSED",
            rho_level=0.99,
            in_domain=(grid.vector_to_matrix(district_array.flatten())==district_dict["DISTRICT_CLOSED"]),
            closed=True
            )
    
    lineouts = {
        "OMP": OMP,
        "IMP": IMP,
        "MP": MP,
        "VMP": VMP,
        "LFS_C0": LFS_C0,
        "LFS_TARGET": LFS_TARGET,
        "HFS_C0": HFS_C0,
        "HFS_TARGET": HFS_TARGET,
        "AX": AX,
        "AXPX": AXPX,
        "AXP0": AXP0,
        "SOL": SOL,
        "SEP": SEP,
        "CLOSED": CLOSED
    }

    return lineouts

def plot_lineouts(lineouts, title):
    flux_surface, _ = FluxSurface(run=run)()
    plt.contour(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(flux_surface.flatten()), 100)

    for lineout in lineouts.values():
        lineout.plot_lineout()

    plt.title(title)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.show()

def setup_results_file(results_file, run, measurement_array, lineouts, snap_indices, time_slice, toroidal_slice, prevent_overwrite=True):
    if prevent_overwrite: assert not(results_file.exists()), f"Error: file {results_file} already exists. Manually remove before continuing"
    
    flux_surface, _ = FluxSurface(run=run)()
    rootgrp = Dataset(results_file, 'w')
        
    rootgrp.createDimension("time", None)
    sample_times = rootgrp.createVariable("times", "f8", ("time",))

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
        for key, interp in lineouts.items():

            lineout_grp = var_grp.createGroup(key)
            lineout_grp.createDimension("points", interp.x_array.size)
            sample_x = lineout_grp.createVariable("x", "f8", ("points",))
            sample_y = lineout_grp.createVariable("y", "f8", ("points",))
            sample_arc = lineout_grp.createVariable("arc", "f8", ("points",))

            if (isinstance(interp, LineInterpolator)):
                sample_rho = lineout_grp.createVariable("rho", "f8", ("points",))
                sample_rho[:] = interp(flux_surface)


            # if (isinstance(interp, FluxSurfaceInterpolator)):
            #     sample_theta = lineout_grp.createVariable("theta", "f8", ("points",))
            #     sample_theta[:] = interp.theta_values()


            val_var = lineout_grp.createVariable("values", "f8", ("time", "points"))

            sample_x[:] = interp.x_array
            sample_y[:] = interp.y_array
            sample_arc[:] = interp.arc_length
            lineout_grp.spatial_factor = run.normalisation.R0.magnitude
            lineout_grp.spatial_factor_units = str(run.normalisation.R0.units)

            lineout_vars[key] = val_var
        
        measurement_vars.append(lineout_vars)

    return measurement_vars

def fill_values(measurement_array, lineouts, measurement_vars, snap_indices, toroidal_slice):

    results = {}
    for measurement, measurement_id in zip(measurement_array, range(len(measurement_array))):
        for key, lineout in lineouts.items():
            results[key] = np.zeros((len(snap_indices), lineout.x_array.size))

        for t, time in zip(range(len(snap_indices)), snap_indices):

            print(f"\tExtracting data at {time} of [{snap_indices[0]}-{snap_indices[-1]}], {measurement.variable.title}")

            results_at_time, _ = measurement.variable(time_slice=[time], toroidal_slice=toroidal_slice)
            
            for key, lineout in lineouts.items():
                results[key][t, :] = lineout(results_at_time)

        for key in lineouts.keys():
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
        # SI_units         = CLI['SI_units']
        # log_scale        = CLI['log_scale']
        # save_path        = CLI['save']

        time_slice       = CLI['time_slice']
        toroidal_slice   = CLI['toroidal_slice']

        run = Run(filepath)

        # Select a list of Variable types to plot
        variables = measurement_groups[group]

        # Construct the list of operators
        operators = []

        # Request the different projectors
        projector = Poloidal()

        measurement_array = measurement_array_from_variable_array(
                                projector=projector,
                                variable_array=variables,
                                reduction=reduction,
                                operators=operators,
                                run=run)
        
        lineouts = setup_lineouts(run)

        # plot_lineouts(lineouts, title)
        # quit()
        
        snap_indices = run.snap_indices[time_slice]

        results_file = Path(filepath)/f"projector_{group}_{snap_indices[0]}_{snap_indices[-1]}.nc"
        
        if not results_file.exists():
            print(f"File {results_file} doesn't exist. Making file now.")

            print("Setting up results file")
            measurement_vars = setup_results_file(
                results_file, run, measurement_array, lineouts, snap_indices, time_slice, toroidal_slice, prevent_overwrite=False)

            print("Filling results file")
            fill_values(measurement_array, lineouts, measurement_vars, snap_indices, toroidal_slice)

        else:
            print(f"File {results_file} exists. Reading from file.")
            rootgrp = Dataset(results_file, 'r')

            density_sol = rootgrp["Density"]["HFS_C0"]

            plt.pcolormesh(density_sol["rho"], rootgrp["times"],
                           density_sol["values"]
                        )

            plt.show()


