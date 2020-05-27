from source import np, plt, perceptually_uniform_cmap, diverging_cmap, mplcolors, Dimensionless, usrenv
# An object which paints a Measurement onto an Axes

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
        self._drawn = False
    
    def draw(self, **kwargs):
        # Keyword arguments must match the arguments for self.measurement.projector.determine_slices
        assert(self.measurement.initialised)

        self.values, self.units = self.measurement(**kwargs)

        if self.colormap is None or self.colormap_norm is None:
            self.find_colormap_normalisation(values=self.values)
        
        self.draw_plot()
        self._drawn = True

    def draw_plot(self):
        raise NotImplementedError(f"{self} has not implemented draw_plot")
    
    def update(self, **kwargs):
        # Update an already-drawn figure with new values
        assert(self.measurement.initialised and self._drawn)
        self.values, self.units = self.measurement(**kwargs)
        self.update_plot()
    
    def clean_frame(self):
        assert(self.measurement.initialised and self._drawn)
        self.image.set_array([])
    
    def update_plot(self):
        raise NotImplementedError(f"{self} has not implemented update_plot")

    @property
    def ax(self):
        return self.axes.ax
    
    @property
    def fig(self):
        return self.canvas.figure.fig
    
    @property
    def projector(self):
        return self.measurement.projector
    
    @property
    def variable(self):
        return self.measurement.variable

    @property
    def x_values(self):
        return self.measurement.projector.x * self.x_normalisation
    
    @property
    def y_values(self):
        return self.measurement.projector.y * self.y_normalisation
    
    @property
    def x_normalisation(self):
        if self.SI_units:
            return self.measurement.projector.x_normalisation
        else:
            return Dimensionless

    @property
    def y_normalisation(self):
        if self.SI_units:
            return self.measurement.projector.y_normalisation
        else:
            return Dimensionless
    
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

        if ((x > self.x_values.magnitude.min()) & (x <= self.x_values.magnitude.max()) &
            (y > self.y_values.magnitude.min()) & (y <= self.y_values.magnitude.max())):
            row = np.searchsorted(self.x_values.magnitude, x)-1
            col = np.searchsorted(self.y_values.magnitude, y)-1
            z = self.values[col, row]

            if self.SI_units:
                x *= self.x_normalisation.units
                y *= self.y_normalisation.units
                z *= self.units

            # See if the field defines a custom formatter for z values. If not, just print the value
            format_value = getattr(self.variable, "__format_value__", None)
            if callable(format_value):
                return f'x={x:f}, y={y:f}, z={format_value(z)}   [{row},{col}]'
            else:
                return f'x={x:f}, y={y:f}, z={z:f}   [{row},{col}]'

        else:
            return 'x={:f}, y={:f}'.format(x, y)
    
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
