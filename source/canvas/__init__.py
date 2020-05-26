from source import np
from .layout import Figure, Axes
from .painter import Painter, Colormesh
from source.measurements import Measurement

class Canvas:

    def __init__(self, figure):
        self.figure = figure

    @classmethod
    def blank_canvas(cls):
        return cls(figure=Figure())

    def draw(self, **kwargs):
        for axes in self.axes_array:
            axes.draw(**kwargs)

    def show(self):
        self.figure.show()

    def add_subplots_from_naxs(self, naxs):
        self.figure.add_subplots_from_naxs(naxs=naxs)
        self.axes_array = self.figure.axes1d

    def add_title(self, title):
        self.figure.make_suptitle(title)
    
    def associate_subplots_with_measurements(self, painter, measurement_array, SI_units=False, log_scale=False, exclude_outliers=False):

        for measurement, axes in zip(measurement_array, self.axes_array):

            axes.painter = painter(canvas=self, measurement=measurement, axes=axes, SI_units=SI_units, log_scale=log_scale, exclude_outliers=exclude_outliers)
        
    def set_SI_units(self, value):
        for axes in self.axes_array:
            axes.SI_units = value
    
    def set_log_scale(self, value):
        for axes in self.axes_array:
            axes.log_scale = value