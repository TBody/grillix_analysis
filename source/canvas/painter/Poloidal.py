from source import matplotlib, np, usrenv
from . import Painter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from copy import deepcopy

class PoloidalPlot(Painter):

    def __init__(self, *args, colorbar_axes=None, **kwargs):
        super().__init__(*args, **kwargs)

        if colorbar_axes is None:
            # create an axes on the right side of ax. The width of cax will be 5%
            # of ax and the padding between cax and ax will be fixed at 0.05 inch.
            divider = make_axes_locatable(self.ax)
            self.colorbar_axes = divider.append_axes("right", size="5%", pad=0.05)
        else:
            self.colorbar_axes = colorbar_axes
        
        self.colorbar = None
    
    def draw_plot(self):

        [values, colormap_norm] = self.convert_to_SI()

        if values.is_vector:
            image = self.draw_quiver(values, colormap_norm)
        else:
            image = self.draw_colormesh(values, colormap_norm)
        
        self.make_colorbar(image, colormap_norm)

        self.annotate_plot()
        self.style_plot()
    
    def convert_to_SI(self):
        # Copy and break reference
        values = deepcopy(self.values)
        colormap_norm = deepcopy(self.colormap_norm)

        if self.SI_units:
            units_magnitude = self.units.magnitude
            values *= units_magnitude
            
            colormap_norm.vmin *= units_magnitude
            colormap_norm.vmax *= units_magnitude
            if hasattr(colormap_norm, "linthres"):
                colormap_norm.linthres *= units_magnitude
        
        return values, colormap_norm

    def plot_in_SI(self, x, y, **kwargs):
        self.ax.plot(x * self.x_normalisation.magnitude, y * self.y_normalisation.magnitude, **kwargs)

    def annotate_plot(self):
        default_linewidth = matplotlib.rcParams['lines.linewidth']

        self.plot_in_SI(self.divertor_polygon.x_points, self.divertor_polygon.y_points, color='b', linewidth=default_linewidth*0.5)
        self.plot_in_SI(self.exclusion_polygon.x_points, self.exclusion_polygon.y_points, color='r', linewidth=default_linewidth*0.5)

        self.seperatrix[0].plot_all_arrays(plot_function=self.plot_in_SI, color='g', linewidth=default_linewidth*0.5)

        self.penalisation_contours[0].plot_all_arrays(plot_function=self.plot_in_SI, color='r', linestyle='--', linewidth=default_linewidth*0.5)
        self.penalisation_contours[-1].plot_all_arrays(plot_function=self.plot_in_SI, color='r', linestyle='--', linewidth=default_linewidth*0.5)

        self.parallel_limit_contours[0].plot_all_arrays(plot_function=self.plot_in_SI, color='b', linestyle='--', linewidth=default_linewidth*0.5)
        self.parallel_limit_contours[1].plot_all_arrays(plot_function=self.plot_in_SI, color='b', linestyle='--', linewidth=default_linewidth*0.5)

    def style_plot(self):
        self.ax.format_coord = self.format_coord
        self.ax.set_aspect('equal')

        self.ax.set_xlim(self.projector.xmin * self.x_normalisation.magnitude, self.projector.xmax * self.x_normalisation.magnitude)
        self.ax.set_ylim(self.projector.ymin * self.y_normalisation.magnitude, self.projector.ymax * self.y_normalisation.magnitude)

        if self.SI_units:
            self.title = self.ax.set_title(f"{self.measurement.title_string()} [{self.units.units}]")
        else:
            self.title = self.ax.set_title(self.measurement.title_string())
    
    def make_colorbar(self, image, colormap_norm):
        
        ticks = np.linspace(start=colormap_norm.vmin, stop=colormap_norm.vmax, num=self.num_cbar_ticks)
        self.colorbar = self.fig.colorbar(image, cax=self.colorbar_axes, ticks=ticks, extend='both' if self.exclude_outliers else 'neither')

    def draw_colormesh(self, values, colormap_norm):
        
        return self.ax.pcolormesh(self.x_values.magnitude, self.y_values.magnitude, values, cmap=self.colormap, norm=colormap_norm)

    def draw_quiver(self, values, colormap_norm):

        max_vector_points = usrenv.max_vector_points_per_dim
        vector_scale_factor = usrenv.vector_scale_factor

        x_samples = np.unique(np.floor(np.linspace(0, 1, num=max_vector_points)*(self.projector.x.size-1))).astype(int)
        y_samples = np.unique(np.floor(np.linspace(0, 1, num=max_vector_points)*(self.projector.y.size-1))).astype(int)

        vector_magnitude = values.vector_magnitude[y_samples,:][:, x_samples]
        
        vector_scale_factor = max_vector_points*np.nanmax(vector_magnitude)/vector_scale_factor

        return self.ax.quiver(self.x_values.magnitude[x_samples],
                               self.y_values.magnitude[y_samples],
                               values.R[y_samples,:][:, x_samples],
                               values.Z[y_samples,:][:, x_samples],
                               vector_magnitude,
                               cmap=self.colormap, norm=colormap_norm,
                               pivot='mid', angles='xy', linewidth=1,
                               scale=vector_scale_factor, scale_units='xy')
        