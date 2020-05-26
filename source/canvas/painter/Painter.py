from source import np, plt, perceptually_uniform_cmap, diverging_cmap, mplcolors
# An object which paints a Measurement onto an Axes

class Painter():

    def __init__(self, canvas, measurement, axes, SI_units=False, log_scale=False):

        self.canvas = canvas
        self.measurement = measurement
        self.axes = axes
        self.SI_units = SI_units
        self._log_scale = log_scale
        
        # Options for colorbar limits
        self.exclude_outliers = False
        # Exclude values outside this quartile range
        self.outliers_quantitles = (0.001, 0.999)

        # Colormap
        self.colormap = perceptually_uniform_cmap
        # Range for color mapping
        self.colormap_norm = None
        # What proportion of a symlog plot should be linear?
        self.linear_proportion = 0.20
        
        self._colormap_calculated = False
    
    def draw(self, **kwargs):
        # Keyword arguments must match the arguments for self.measurement.projector.determine_slices
        assert(self.measurement.initialised)

        self.values, self.units = self.measurement(**kwargs)

        if self.colormap is None or self.colormap_norm is None:
            self.find_colormap_normalisation(values=self.values)
        
        self.draw_plot(axes=self.axes, values=self.values, units=self.units)
    
    def draw_plot(self, axes, values, units):
        raise NotImplementedError(f"{self} has not implemented draw_plot")
    
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
        self.axes.ax.clear()
        self.axes.ax.set_axis_off()
        self.axes.ax.set_frame_on(False)
    
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

    def style_plot(self, axes, values, units):
        axes.ax.format_coord = self.format_coord
        axes.ax.set_aspect('equal')

        axes.ax.plot(self.divertor_polygon.x_points, self.divertor_polygon.y_points, color='b')
        axes.ax.plot(self.exclusion_polygon.x_points, self.exclusion_polygon.y_points, color='r')

        self.seperatrix[0].plot_all_arrays(plot_function=axes.ax.plot, color='g')

        self.penalisation_contours[0].plot_all_arrays(plot_function=axes.ax.plot, color='r', linestyle='--')
        self.penalisation_contours[-1].plot_all_arrays(plot_function=axes.ax.plot, color='r', linestyle='--')

        self.parallel_limit_contours[0].plot_all_arrays(plot_function=axes.ax.plot, color='b', linestyle='--')
        self.parallel_limit_contours[1].plot_all_arrays(plot_function=axes.ax.plot, color='b', linestyle='--')

        axes.ax.set_xlim(left=self.run.grid.xmin, right=self.run.grid.xmax)
        axes.ax.set_ylim(bottom=self.run.grid.ymin, top=self.run.grid.ymax)

class Colormesh(Poloidal):

    def draw_plot(self, axes, values, units):

        axes.ax.pcolormesh(self.x_values, self.y_values, values, cmap=self.colormap, norm=self.colormap_norm)
        
        self.style_plot(axes, values, units)
        