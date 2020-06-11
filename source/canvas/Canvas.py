from source import np, plt, Dimensionless, usrenv, warnings
from .Painter import Painter, PoloidalPlot
from .Colorbar import Colorbar
from .Title import Title

class Canvas:
    # Similar to matplotlib.figure, with extended methods to allow easier plotting and animation

    def __init__(self, **kwargs):
        self.fig = plt.figure(**kwargs)

    def show(self):
        plt.show()
    
    def determine_layout(self, naxs):
        if naxs <= 0:
            raise NotImplementedError(f"No figure generated for naxs = {naxs}")
        elif naxs <= 3:
            nrows = 1
            ncols = naxs
        elif naxs == 4:
            nrows = 2
            ncols = 2
        elif naxs <= 6:
            nrows = 2
            ncols = 3
        elif naxs <= 8:
            nrows = 2
            ncols = 4
        elif naxs <= 10:
            nrows = 2
            ncols = 5
        else:
            raise NotImplementedError(f"No figure generated for naxs = {naxs}")
        
        return nrows, ncols
    
    def __getattr__(self, key):
        try:
            return getattr(self.fig, key)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {key}")

    def subplots_from_naxs(self, naxs, sharex=True, sharey=True, squeeze=False, subplot_kw=None, gridspec_kw=None):
        [nrows, ncols] = self.determine_layout(naxs)
        return self.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, squeeze=False, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)

    def subplots(self, nrows=1, ncols=1, sharex=True, sharey=True, squeeze=False, subplot_kw=None, gridspec_kw=None):
        return self.fig.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, squeeze=False, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)
    
    def subplots_from_measurement_array(self, painter, measurement_array, run=None, SI_units=False, log_scale=False, exclude_outliers=False, cbar_in_vessel=True, **subplot_kw):
        assert(type(painter) is type)

        subplots = self.subplots_from_naxs(naxs=len(measurement_array), **subplot_kw)
        self.axes = []

        for measurement, subplot in zip(measurement_array, subplots.flatten()):

            painter_object = painter(axes=subplot, measurement=measurement, run=run, SI_units=SI_units)
            cbar_object, _ = Colorbar.make_colorbar_axis(painter=painter_object, run=run, log_scale=log_scale, exclude_outliers=exclude_outliers, cbar_in_vessel=cbar_in_vessel)

            self.axes.append(painter_object)
            self.axes.append(cbar_object)
    
    def title(self, title_string, SI_units=False, run=None):
        title_object, _ = Title.make_title_axes(canvas=self, title_string=title_string, SI_units=SI_units, run=run)

        self.axes.append(title_object)
    
    def draw(self, **kwargs):
        
        for axes in self.axes:
            axes.draw(**kwargs)
        
    def tight_layout(self):
        # Leave space for the suptitle
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            plt.tight_layout(rect=[0, 0, 1, 1-usrenv.suptitle_vspace])
    
    def save_figure(self, filename):
        plt.savefig(f"{filename}")

    def set_SI_units(self, value):
        for axes in self.axes:
            axes.SI_units = value

    def set_log_scale(self, value):
        for axes in self.axes:
            axes.log_scale = value

    from ._animation import update, clean_frame, find_static_colormap, return_animation_artists, make_animator, save_animation