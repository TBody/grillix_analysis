from source import plt, Component
from .Painter._artists import Artist

class Axes(Component):
    # Axes are components, but it's OK if they're used uninitialised (i.e. with no run object given)

    @classmethod
    def rect(cls, xmin, xmax, ymin, ymax):
        # axis limits should be given in terms of figure fractions

        left = xmin
        bottom = ymin
        width = xmax - xmin
        height = ymax - ymin

        return cls(plt.axes([left, bottom, width, height]))
    
    def __init__(self, ax):
        self.ax = ax
    
    def draw(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented draw")

    def clear(self):
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_frame_on(False)
    
class AnimatedAxis(Axes):

    def __init__(self, ax):
        super().__init__(ax)
        self.artist = Artist()

    def update(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented update")

    def clear_frame(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented clear_frame")

    def return_artist(self):
        return self.artist