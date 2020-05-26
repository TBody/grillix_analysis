from source import np, plt, Dimensionless
from .. import Component
from .layout import Figure, Axes
from .painter import Painter, PoloidalPlot
from source.measurements import Measurement

class Canvas(Component):

    def __init__(self, figure, run=None):
        self.figure = figure
        self.run = run

    @classmethod
    def blank_canvas(cls):
        return cls(figure=Figure())

    def draw(self, with_tight_layout=True, **kwargs):
        for axes in self.axes_array:
            axes.draw(**kwargs)
        
        self.add_time_to_title(**kwargs)

        if with_tight_layout:
            # Leave space for the suptitle
            plt.tight_layout(rect=[0, 0, 1, 0.95])

    def show(self):
        self.figure.show()

    def add_subplots_from_naxs(self, naxs):
        self.figure.add_subplots_from_naxs(naxs=naxs)
        self.axes_array = self.figure.axes1d

    def add_title(self, title, title_SI=False):
        self.title_text = title
        self.title_SI = title_SI
        self.figure.make_suptitle(self.title_text)
    
    def add_time_to_title(self, time_slice=slice(-1,None), **kwargs):
        tau_normalisation = self.normalisation.tau_0 if self.title_SI else Dimensionless
        tau_values = np.atleast_1d(self.run.tau_values[time_slice])*tau_normalisation

        self.figure.suptitle_time = tau_values
    
    def associate_subplots_with_measurements(self, painter, measurement_array, SI_units=False, log_scale=False, exclude_outliers=False):

        for measurement, axes in zip(measurement_array, self.axes_array):

            axes.painter = painter(canvas=self, measurement=measurement, axes=axes, SI_units=SI_units, log_scale=log_scale, exclude_outliers=exclude_outliers)
        
    def set_SI_units(self, value):
        for axes in self.axes_array:
            axes.SI_units = value
    
    def set_log_scale(self, value):
        for axes in self.axes_array:
            axes.log_scale = value
    
    def save(self, filename):
        plt.savefig(f"{filename}", transparent=True)