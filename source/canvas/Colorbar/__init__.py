from source import usrenv, perceptually_uniform_cmap, np, plt
from ..Axes import Axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
from copy import deepcopy

class Colorbar(Axes):

    @classmethod
    def make_colorbar_axis(cls, painter, **kwargs):
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(painter.ax)

        axes = divider.append_axes("right", size="5%", pad=0.05)

        return cls(axes, painter=painter, **kwargs), axes

    def __init__(self, axes, painter=None, log_scale=False, exclude_outliers=False, run=None):

        super().__init__(axes)

        self.painter = painter

        # Use a logarithmic colormap
        self.log_scale = log_scale
        # Exclude outermost quartiles of data from the colormap
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

    @property
    def painter(self):
        if self._painter is None:
            raise RuntimeError(f"Painter has not yet been set")
        else:
            return self._painter
    
    @painter.setter
    def painter(self, value):
        self._painter = value
        if self._painter is not None:
            self._painter._colorbar = self

    @property
    def SI_units(self):
        return self.painter.SI_units
    
    @property
    def colormap_norm(self):

        if self._colormap_norm is None:
            self.find_colormap_normalisation(values=self.painter._values)

        if self.SI_units:
            colormap_norm = deepcopy(self._colormap_norm)
            units_magnitude = self.painter.units.magnitude
            
            colormap_norm.vmin *= units_magnitude
            colormap_norm.vmax *= units_magnitude
            if hasattr(colormap_norm, "linthres"):
                colormap_norm.linthres *= units_magnitude
            
            return colormap_norm
        else:
            return self._colormap_norm
    
    @colormap_norm.setter
    def colormap_norm(self, value):
        self._colormap_norm = value
    
    def draw(self, **kwargs):
        colormap_norm = self.colormap_norm
    
        ticks = np.linspace(start=colormap_norm.vmin, stop=colormap_norm.vmax, num=self.num_cbar_ticks)
        self.colorbar = plt.colorbar(self.painter.artist, cax=self.ax, ticks=ticks, extend='both' if self.exclude_outliers else 'neither')

    @property
    def allow_diverging_cmap(self):
        return self.painter.measurement.variable.allow_diverging_cmap

    from ._find_colormap import find_static_colormap_normalisation, find_colormap_normalisation, data_limits