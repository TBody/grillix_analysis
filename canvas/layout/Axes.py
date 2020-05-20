from source import plt

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