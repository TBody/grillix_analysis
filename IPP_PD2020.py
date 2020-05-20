#!/usr/bin/env python
# Import CLI user interface
from interface.CLI import (
    BaseCLI,
    FilepathArg, SaveFilepathArg,
    TitleArg,
    TimeSliceArg,
    ConvertToSIArg, DisplayLogarithmArg
)

# Set up command-line interface
class PD2020_CLI(BaseCLI):

    def __init__(self, parse=False, display=False):
        super().__init__("Animate values over a poloidal plane (for program day 2020)")

        self.filepath           = FilepathArg(self)
        self.save               = SaveFilepathArg(self)
        self.title              = TitleArg(self)
        self.time_slice         = TimeSliceArg(self, default_all=True, allow_range=True, allow_step=True)
        self.display_logarithm  = DisplayLogarithmArg(self)

        if parse: self.parse()
        if display: print(self)

# import the necessary components from source
from source.Run import Run
from source.Projector.Poloidal import Poloidal
from ipdb import launch_ipdb_on_exception
from source.shared import check_ffmpeg
from source import plt, np, perceptually_uniform_cmap, mplcolors, Quantity, matplotlib
from matplotlib import animation
from source.interface import UserEnvironment

def find_omp(grid, rho, plot=False):
    # Find the axis position for the OMP profile

    [x_mesh, y_mesh] = np.meshgrid(grid.x_unique, grid.y_unique)

    rho_values = rho().values.flatten()
    # axis_index = np.nanargmin(rho_values)
    # x_axis = grid.x[axis_index]
    # y_axis = grid.y[axis_index]
    x_axis = Quantity(2.02, 'm')
    y_axis = Quantity(0.08, 'm')

    x_axis_index = np.nanargmin(np.abs(x_axis-grid.x_unique))
    y_axis_index = np.nanargmin(np.abs(y_axis-grid.y_unique))

    omp_slice = (y_axis_index, slice(x_axis_index, None))
    x_omp = x_mesh[omp_slice]
    y_omp = y_mesh[omp_slice]
    rho_omp = grid.vector_to_matrix(rho_values)[omp_slice]

    if plot:
        plt.plot(x_omp, y_omp, label="y")
        plt.plot(x_omp, rho_omp, label="rho")
        plt.legend()
        plt.show()

    return rho_omp, omp_slice, x_omp, y_omp

def add_time_to_title(suptitle, title_text, convert, run, time_slice):

    tau_values = np.atleast_1d(run.tau_values[time_slice])

    if len(tau_values) > 1:
        if convert:
            suptitle.set_text(f"{title_text} [t = {tau_values[0].to_compact():4.3f} to {tau_values[-1].to_compact():4.3f}]")
        else:
            suptitle.set_text(f"{title_text} [{tau_values[0]:4.3f} to {tau_values[-1]:4.3f} tau]")
    else:
        if convert:
            suptitle.set_text(f"{title_text} [t = {tau_values[0].to_compact():4.3f}]")
        else:
            suptitle.set_text(f"{title_text} [{tau_values[0]:4.3f} tau]")

def find_electric_field_profile(grid, radial, electric_field, omp_slice, time_slice=slice(-1,None), toroidal_slice=slice(None)):
    radial_electric_field = radial(electric_field(time_slice=time_slice, toroidal_slice=toroidal_slice))
    electric_field_omp = grid.vector_to_matrix(radial_electric_field)[:, :, omp_slice[0], omp_slice[1]]
    return electric_field_omp

def find_reduced_electric_field_profile(projector, radial, electric_field, omp_slice, time_slice=slice(-1,None), toroidal_slice=slice(None)):
    return projector.structure_z(radial(electric_field(time_slice=time_slice, toroidal_slice=toroidal_slice)))[omp_slice]

def find_pressure_profile(grid, pressure, omp_slice, time_slice=slice(-1,None), toroidal_slice=slice(None)):
    total_pressure = pressure(time_slice=time_slice, toroidal_slice=toroidal_slice)
    pressure_omp = grid.vector_to_matrix(total_pressure)[:, :, omp_slice[0], omp_slice[1]]
    return pressure_omp

def find_reduced_pressure_profile(projector, pressure, omp_slice, time_slice=slice(-1,None), toroidal_slice=slice(None)):
    return projector.structure_z(pressure(time_slice=time_slice, toroidal_slice=toroidal_slice))[omp_slice]

def axis_layout_rectangle(left, bottom, width, height):
    return [left, bottom, width, height]

def annotate_figure(run, ax, x_omp, y_omp, linestyle='-', linewidth=2):
    run.divertor_polygon.plot(ax, color='b', linestyle=linestyle, linewidth=linewidth)
    run.seperatrix[0].plot(ax, color='g', linestyle=linestyle, linewidth=linewidth)
    plt.plot(x_omp, y_omp, color='r', linestyle='--', linewidth=1)

def find_cmap_limits(result):
    result_min = np.nanmin(result.magnitude.ravel())
    result_max = np.nanmax(result.magnitude.ravel())
    
    return result_min, result_max

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset, inset_axes

if __name__=="__main__":
    # Wrapping everything with "with launch_ipdb_on_exception():" has the helpful effect that, upon a crash, the ipdb debugger is launched
    # so you can find out what went wrong
    with launch_ipdb_on_exception():
        check_ffmpeg()
        font = {'size'   : 18}
        matplotlib.rc('font', **font)
        # CLI behaves exactly like a dictionary. If you want, you can modify it with standard dictionary methods, or replace it altogether
        CLI = PD2020_CLI(parse=True, display=True)

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
        run.convert = True

        # Select a list of Variable types to animate
        from source.Variable import Density, ElectricField, FluxSurface, TotalPressure
        from source.measurements.Operator import AllReduction, VectorRadialProjection
        # For this analysis, we just want the density and the radially-projected electric fieldu

        # Need to specify the limits of the OMP by hand
        omp = {
            'xmin': 2.0,
            'xmax': 2.18,
            'ymin': -0.1,
            'ymax': 0.25
        }
        xpt = {
            'xmin': 1.33,
            'xmax': 1.6,
            'ymin': -1.1,
            'ymax': -0.8
        }
        
        grid = run.grid
        density = Density(run=run)
        electric_field = ElectricField(run=run)
        pressure = TotalPressure(run=run)
        radial = VectorRadialProjection(run=run)
        rho = FluxSurface(run=run)
        allreduce = AllReduction()
        mask = run.in_vessel_mask.astype(float)
        mask[np.logical_not(run.in_vessel_mask)] = np.nan
        mask = grid.vector_to_matrix(mask)

        [x_mesh, y_mesh] = np.meshgrid(grid.x_unique, grid.y_unique)

        # Request the 'Poloidal' projector. A projector takes z(t, phi, l) and maps it to a 2D array, in this case z(x, y)
        # The treatment of the 't' and 'phi' axis is via an AllReduction operator, passed as the reduction keyword
        projector = Poloidal(reduction=allreduce, run=run)

        [rho_omp, omp_slice, x_omp, y_omp] = find_omp(run.grid, rho, plot=False)

        def electric_field_profile_at_t(time_slice=slice(-1, None), reduction=True):
            if reduction:
                return find_reduced_electric_field_profile(projector, radial, electric_field, omp_slice, time_slice)
            else:
                return find_electric_field_profile(grid, radial, electric_field, omp_slice, time_slice)
        
        def pressure_profile_at_t(time_slice=slice(-1, None), reduction=True):
            if reduction:
                return find_reduced_pressure_profile(projector, pressure, omp_slice, time_slice)
            else:
                return find_pressure_profile(grid, pressure, omp_slice, time_slice)
        
        def density_at_t(time_slice=slice(-1, None)):
            return mask*projector.structure_z(density(time_slice=time_slice, toroidal_slice=[0]))

        time_slice = ctrl['time_slice']
        # Take every 10th value
        time_slice_stepped = slice(time_slice.start, time_slice.stop, 20)

        [density_min, density_max] = find_cmap_limits(density_at_t(time_slice=time_slice_stepped).values)
        density_norm = mplcolors.Normalize(vmin=density_min, vmax=density_max)
        [Efield_min, Efield_max] = find_cmap_limits(electric_field_profile_at_t(time_slice=time_slice_stepped, reduction=False))
        [Pressure_min, Pressure_max] = find_cmap_limits(pressure_profile_at_t(time_slice=time_slice_stepped, reduction=False))

        # Arrange the figure layout
        fig = plt.figure(figsize=(12, 13))

        main_axis_bottom = 0.25
        main_axis_height = 0.65
        main_axis_left   = 0.25
        main_axis_width  = 0.4
        divertor_limits = {'xmin': np.min(run.divertor_polygon.x_points), 'xmax': np.max(run.divertor_polygon.x_points),
                           'ymin': np.min(run.divertor_polygon.y_points), 'ymax': np.max(run.divertor_polygon.y_points)}

        main_density_axis = plt.axes(axis_layout_rectangle(left=main_axis_left, bottom=main_axis_bottom, width=main_axis_width, height=main_axis_height))

        main_title = main_density_axis.set_title("", pad=20)

        main_density_plot = main_density_axis.pcolormesh(projector.x, projector.y, density_at_t(), cmap=perceptually_uniform_cmap, norm=density_norm)
        annotate_figure(run, main_density_axis, x_omp, y_omp)
        main_density_axis.set_aspect("equal", adjustable='box', anchor='C')
        main_density_axis.set_xlim(left=divertor_limits['xmin'], right=divertor_limits['xmax'])
        main_density_axis.set_ylim(bottom=divertor_limits['ymin'], top=divertor_limits['ymax'])

        omp_density_inset = inset_axes(main_density_axis, width='80%', height='80%', loc="center",
            bbox_to_anchor=(1.05, 0.12, 1, 1), bbox_transform=main_density_axis.transAxes
        )

        density_omp_plot = omp_density_inset.pcolormesh(projector.x, projector.y, density_at_t(), cmap=perceptually_uniform_cmap, norm=density_norm)
        omp_density_inset.set_aspect("equal")
        annotate_figure(run, omp_density_inset, x_omp, y_omp)

        omp_density_inset.set_xlim(omp['xmin'], omp['xmax'])
        omp_density_inset.set_ylim(omp['ymin'], omp['ymax'])
        omp_density_inset.xaxis.set_visible(False)
        omp_density_inset.yaxis.set_visible(False)
        mark_inset(main_density_axis, omp_density_inset, loc1=2, loc2=3, fc="none", ec="0.5")

        xpt_density_inset = inset_axes(main_density_axis, width='80%', height='100%', loc="center",
            bbox_to_anchor=(1.05, -0.57, 1, 1), bbox_transform=main_density_axis.transAxes
        )

        density_xpt_plot = xpt_density_inset.pcolormesh(projector.x, projector.y, density_at_t(), cmap=perceptually_uniform_cmap, norm=density_norm)
        xpt_density_inset.set_aspect("equal")
        annotate_figure(run, xpt_density_inset, x_omp, y_omp)

        xpt_density_inset.set_xlim(xpt['xmin'], xpt['xmax'])
        xpt_density_inset.set_ylim(xpt['ymin'], xpt['ymax'])
        xpt_density_inset.xaxis.set_visible(False)
        xpt_density_inset.yaxis.set_visible(False)
        mark_inset(main_density_axis, xpt_density_inset, loc1=2, loc2=3, fc="none", ec="0.5")

        colorbar_axis = plt.axes(axis_layout_rectangle(left=0.1, bottom=main_axis_bottom, width=0.05, height=main_axis_height))

        cbar = plt.colorbar(main_density_plot, cax=colorbar_axis)
        colorbar_axis.yaxis.set_label_position('left')
        cbar.set_label('Density [per cubic meter]', rotation=90)

        electric_field_axis = plt.axes(axis_layout_rectangle(left=main_axis_left-0.15, bottom=0.06, width=main_axis_width+0.05, height=0.1))
        pressure_axis = electric_field_axis.twinx()

        electric_field_plot = electric_field_axis.plot(rho_omp, electric_field_profile_at_t(), 'r')[0]
        electric_field_axis.set_ylim(bottom=Efield_min, top=Efield_max)
        electric_field_axis.set_ylabel("E radial [kV/m]", color='r')
        electric_field_axis.tick_params(axis='y', labelcolor='r')
        
        pressure_plot = pressure_axis.semilogy(rho_omp, pressure_profile_at_t(), 'b')[0]
        pressure_axis.set_yticks([1E-3, 1E-0])
        pressure_axis.set_ylim(bottom=Pressure_min, top=Pressure_max)
        pressure_axis.set_ylabel("Pressure [kPa]", color='b', rotation=270, labelpad=20)
        pressure_axis.tick_params(axis='y', labelcolor='b')
        
        from matplotlib.ticker import FormatStrFormatter
        electric_field_axis.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        electric_field_axis.xaxis.set_major_locator(plt.MaxNLocator(3))
        electric_field_axis.set_xlabel("Normalised pol. flux")
        electric_field_axis.set_title("OMP Profile")
        electric_field_axis.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
        electric_field_axis.axvline(x=1, color='g', linestyle='--', linewidth=1)

        def title_at_time(time_slice=slice(-1, None)):
            add_time_to_title(main_title, ctrl["title"], run.convert, run, time_slice)

        title_at_time()

        # Read the tau values to determine how many snaps to plot
        snap_indices = run.snap_indices[ctrl["time_slice"]]

        def animate(t):
            print(f"\tMaking frame {t} of [{snap_indices[0]}-{snap_indices[-1]}]")
            
            density_frame = density_at_t(t).values.magnitude
            electric_frame = electric_field_profile_at_t(t).magnitude
            pressure_frame = pressure_profile_at_t(t).magnitude

            main_density_plot.set_array(density_frame[:-1, :-1].ravel())
            density_omp_plot.set_array(density_frame[:-1, :-1].ravel())
            density_xpt_plot.set_array(density_frame[:-1, :-1].ravel())
            electric_field_plot.set_ydata(electric_frame)
            pressure_plot.set_ydata(pressure_frame)

            title_at_time(t)

            return main_density_plot, density_omp_plot, density_xpt_plot, electric_field_plot, pressure_plot, main_title,


        animator = animation.FuncAnimation(fig, animate, frames=snap_indices, blit=False, repeat = True, interval = 1, cache_frame_data=False)

        # The animation layout may be different to the interactive plot layout. Use a test figure to fine-tune layout if the animation does not look as expected
        # plt.savefig("Test.png")
        # quit()

        if ctrl["save"]:
            usrenv = UserEnvironment()

            # writer = animation.FFMpegWriter(fps=usrenv.animation_framerate,
            #                                 metadata=dict(artist=usrenv.author_name),
            #                                 bitrate=usrenv.animation_bitrate,
            #                                 codec=usrenv.animation_codec)

            writer = animation.FFMpegFileWriter(fps=usrenv.animation_framerate,
                                            metadata=dict(artist=usrenv.author_name),
                                            bitrate=usrenv.animation_bitrate,
                                            codec=usrenv.animation_codec)
            
            animation_filename = ctrl["save"].with_suffix('.'+usrenv.animation_format)

            print(f"Saving video as {animation_filename}")
            animator.save(animation_filename, writer=writer, dpi=usrenv.animation_dpi)
            # animator.save(animation_filename, writer=writer, dpi=fig.dpi)
            print("Done")
        else:
            plt.show()
