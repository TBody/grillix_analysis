from source import np
from ..Axes import AnimatedAxes
from ._artists import Artist

class Painter(AnimatedAxes):

    def __init__(self, axes, measurement, run=None, SI_units=False):

        super().__init__(axes)

        self.measurement = measurement
        self.SI_units = SI_units
        self.artist = Artist()
        self.annotations = []

        self.run = run
        self._drawn = False

    from ._properties import projector, variable, x_values, y_values, x_normalisation, y_normalisation

    @property
    def values(self):
        if self.SI_units:
            return self._values * self.units.magnitude
        else:
            return self._values
    
    @values.setter
    def values(self, value):
        self._values = value

    def draw(self, **kwargs):
        # Keyword arguments must match the arguments for self.measurement.projector.determine_slices
        assert(self.measurement.initialised)

        self.values, self.units = self.measurement(**kwargs)
        self.draw_plot()

        self._drawn = True

    def draw_plot(self):
        raise NotImplementedError(f"{self} has not implemented draw_plot")

    def update(self, **kwargs):
        # Update an already-drawn figure with new values
        assert(self.measurement.initialised and self._drawn)
        self.values, self.units = self.measurement(**kwargs)
        self.artist.update_values()

    def update_plot(self):
        raise NotImplementedError(f"{self} has not implemented update_plot")

    def clean_frame(self):
        assert(self.measurement.initialised and self._drawn)
        self.artist.set_blank_data()

    def format_coord(self, x, y):

        if ((x > self.x_values.magnitude.min()) & (x <= self.x_values.magnitude.max()) &
            (y > self.y_values.magnitude.min()) & (y <= self.y_values.magnitude.max())):
            row = np.searchsorted(self.x_values.magnitude, x)-1
            col = np.searchsorted(self.y_values.magnitude, y)-1
            z = self.values[col, row]

            if self.SI_units:
                x *= self.x_normalisation.units
                y *= self.y_normalisation.units
                z *= self.units.units

            # See if the field defines a custom formatter for z values. If not, just print the value
            format_value = getattr(self.variable, "__format_value__", None)
            if callable(format_value):
                return f'x={x:f}, y={y:f}, z={format_value(z)}   [{row},{col}]'
            else:
                return f'x={x:f}, y={y:f}, z={z:f}   [{row},{col}]'

        else:
            return 'x={:f}, y={:f}'.format(x, y)

    def return_artist(self):
        if self.artist:
            return self.artist
        else:
            raise RuntimeError(f"Artist has not yet been set")

from .PoloidalPlot import PoloidalPlot