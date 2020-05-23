from source import np
from .layout import Figure, Axes
from .painter import Painter, Colormesh
from source.measurements import Measurement

class Canvas:

    def __init__(self, figure, SI_units, log_scale, run=None):
        self.figure = figure
        self.SI_units = SI_units
        self.log_scale = log_scale

        self.run = run
    
    @classmethod
    def blank_canvas(cls, SI_units=False, log_scale=False, run=None):
        return cls(figure=Figure(), SI_units=SI_units, log_scale=log_scale, run=run)

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
    
    def associate_subplots_with_measurements(self, painter, measurement_array):

        for measurement, axes in zip(measurement_array, self.axes_array):

            axes.painter = painter(measurement=measurement, axes=axes)
        
    