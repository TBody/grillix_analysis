from source import plt
from ..painter import Painter

class Axes:

    @classmethod
    def rect(cls, xmin, xmax, ymin, ymax, **kwargs):
        # axis limits should be given in terms of figure fractions

        left = xmin
        bottom = ymin
        width = xmax - xmin
        height = ymax - ymin

        return cls(plt.axes([left, bottom, width, height], **kwargs))
    
    @classmethod
    def auto(cls, **kwargs):
        # axis limits should be given in terms of figure fractions

        return cls(plt.axes(**kwargs))

    def __init__(self, ax, **kwargs):

        self.ax = ax
        self.painter = []
    
    def draw(self, **kwargs):
        if self.painter:
            self.painter.draw(**kwargs)
        else:
            self.clear()
    
    def update(self, **kwargs):
        if self.painter:
            self.painter.update(**kwargs)

    def clear(self):
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_frame_on(False)
    
    def return_artist(self):
        if self.painter:
            return self.painter.image
        else:
            return []