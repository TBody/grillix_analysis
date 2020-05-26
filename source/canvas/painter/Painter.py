from source import np, plt, perceptually_uniform_cmap, diverging_cmap, mplcolors, matplotlib, UserEnvironment
# An object which paints a Measurement onto an Axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
from copy import deepcopy

usrenv = UserEnvironment()

class Painter():

    def __init__(self, canvas, measurement, axes, SI_units=False, log_scale=False, exclude_outliers=False):
        
        self.canvas = canvas
        self.measurement = measurement
        self.axes = axes
        self.SI_units = SI_units
        self._log_scale = log_scale
        
        # Options for colorbar limits
        self.exclude_outliers = exclude_outliers
        # Exclude values outside this quartile range
        self.outliers_quantitles = usrenv.exclude_outliers_quantiles

        # Colormap
        self.colormap = perceptually_uniform_cmap
        # Range for color mapping
        self.colormap_norm = None
        # What proportion of a symlog plot should be linear?
        self.linear_proportion = 0.20
        # How many ticks to label? Should always be odd to get centre value
        self.num_cbar_ticks = 7
        
        self._colormap_calculated = False
    
    def draw(self, **kwargs):
        # Keyword arguments must match the arguments for self.measurement.projector.determine_slices
        assert(self.measurement.initialised)

        self.values, self.units = self.measurement(**kwargs)

        if self.colormap is None or self.colormap_norm is None:
            self.find_colormap_normalisation(values=self.values)
        
        self.image = self.draw_plot()

    def draw_plot(self):
        raise NotImplementedError(f"{self} has not implemented draw_plot")
    
    @property
    def ax(self):
        return self.axes.ax
    
    @property
    def fig(self):
        return self.canvas.figure.fig

    @property
    def x_values(self):
        return self.measurement.projector.x
    
    @property
    def y_values(self):
        return self.measurement.projector.y
    
    @property
    def log_scale(self):
        return self._log_scale
    
    @log_scale.setter
    def log_scale(self, value):
        if self._colormap_calculated:
            print("Warning: log_scale set after colormap was calculated. Need to recalculate colormaps")
        self._log_scale = value
    
    from ._colormaps import (find_static_colormap_normalisation, find_colormap_normalisation, data_limits)

    def format_coord(self, x, y):

        if ((x > self.x_values.min()) & (x <= self.x_values.max()) &
            (y > self.y_values.min()) & (y <= self.y_values.max())):
            row = np.searchsorted(self.x_values, x)-1
            col = np.searchsorted(self.y_values, y)-1
            z = self.values[col, row]

            # See if the field defines a custom formatter for z values. If not, just print the value
            format_value = getattr(self.measurement.variable, "__format_value__", None)
            if callable(format_value):
                return f'x={x:f}, y={y:f}, z={format_value(z)}   [{row},{col}]'
            else:
                return f'x={x:f}, y={y:f}, z={z:f}   [{row},{col}]'

        else:
            return 'x={:f}, y={:f}'.format(x, y)
    
    def clear(self):
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_frame_on(False)
    
    @property
    def run(self):
        return self.measurement.run
    
    @property
    def divertor_polygon(self):
        return self.measurement.run.divertor_polygon
    
    @property
    def exclusion_polygon(self):
        return self.measurement.run.exclusion_polygon
    
    @property
    def seperatrix(self):
        return self.measurement.run.seperatrix

    @property
    def penalisation_contours(self):
        return self.measurement.run.penalisation_contours

    @property
    def parallel_limit_contours(self):
        return self.measurement.run.parallel_limit_contours

class Poloidal(Painter):

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

    def style_plot(self):
        self.ax.format_coord = self.format_coord
        self.ax.set_aspect('equal')

        default_linewidth = matplotlib.rcParams['lines.linewidth']

        self.ax.plot(self.divertor_polygon.x_points, self.divertor_polygon.y_points, color='b', linewidth=default_linewidth*0.5)
        self.ax.plot(self.exclusion_polygon.x_points, self.exclusion_polygon.y_points, color='r', linewidth=default_linewidth*0.5)

        self.seperatrix[0].plot_all_arrays(plot_function=self.ax.plot, color='g', linewidth=default_linewidth*0.5)

        self.penalisation_contours[0].plot_all_arrays(plot_function=self.ax.plot, color='r', linestyle='--', linewidth=default_linewidth*0.5)
        self.penalisation_contours[-1].plot_all_arrays(plot_function=self.ax.plot, color='r', linestyle='--', linewidth=default_linewidth*0.5)

        self.parallel_limit_contours[0].plot_all_arrays(plot_function=self.ax.plot, color='b', linestyle='--', linewidth=default_linewidth*0.5)
        self.parallel_limit_contours[1].plot_all_arrays(plot_function=self.ax.plot, color='b', linestyle='--', linewidth=default_linewidth*0.5)

        self.ax.set_xlim(left=self.run.grid.xmin, right=self.run.grid.xmax)
        self.ax.set_ylim(bottom=self.run.grid.ymin, top=self.run.grid.ymax)
    
    def make_colorbar(self, image, colormap_norm):
        
        ticks = np.linspace(start=colormap_norm.vmin, stop=colormap_norm.vmax, num=self.num_cbar_ticks)
        self.colorbar = self.fig.colorbar(image, cax=self.colorbar_axes, ticks=ticks, extend='both' if self.exclude_outliers else 'neither')

class Colormesh(Poloidal):

    def draw_plot(self):

        # import ipdb; ipdb.set_trace()
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

        image = self.ax.pcolormesh(self.x_values, self.y_values, values, cmap=self.colormap, norm=colormap_norm)
        
        self.make_colorbar(image, colormap_norm)

        self.style_plot()
        
        return image