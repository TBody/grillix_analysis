from source import plt
# An object which paints a Measurement onto an Axes

class Painter():

    def __init__(self, measurement, axes):

        self.measurement = measurement
        self.axes = axes
    
    def draw(self, **kwargs):
        # Keyword arguments must match the arguments for self.measurement.projector.determine_slices
        assert(self.measurement.initialised)

        values, units =self.measurement(**kwargs)
        
        self.draw_plot(axes=self.axes, values=values, units=units)
    
    def draw_plot(self, axes, values):
        raise NotImplementedError(f"{self} has not implemented draw_plot")
    
    @property
    def x_values(self):
        return self.measurement.projector.x
    
    @property
    def y_values(self):
        return self.measurement.projector.y

class Colormesh(Painter):

    def draw_plot(self, axes, values, units):
        
        axes.ax.pcolormesh(self.x_values, self.y_values, values)