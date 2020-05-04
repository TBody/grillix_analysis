from . import Annotate

class PoloidalAnnotate(Annotate):

    def __init__(self, **kwargs):
        self.initialised = False

    def __call__(self, subplot, linestyle='-', linewidth=0.5):
        assert(self.initialised), f"Annotate called before supplying Run values"
        
        self.run.penalisation_contours[0].plot(subplot.ax, color='r', linestyle=linestyle, linewidth=linewidth)
        self.run.penalisation_contours[-1].plot(subplot.ax, color='r', linestyle=linestyle, linewidth=linewidth)
        
        self.run.divertor_polygon.plot(subplot.ax, color='b', linestyle=linestyle, linewidth=linewidth)
        self.run.exclusion_polygon.plot(subplot.ax, color='g', linestyle=linestyle, linewidth=linewidth)
        
        self.run.seperatrix[0].plot(subplot.ax, color='g', linestyle=linestyle, linewidth=linewidth)

        subplot.ax.set_xlim(left=self.run.grid.xmin, right=self.run.grid.xmax)
        subplot.ax.set_ylim(bottom=self.run.grid.ymin, top=self.run.grid.ymax)
        
    def label_axes(self, subplot):
        if not(subplot.hide_xlabel):
            if subplot.convert:
                subplot.ax.set_xlabel(f"R [{self.run.normalisation.R0.units}]")
            else:
                subplot.ax.set_xlabel(f"R/R0")
            
        if not(subplot.hide_ylabel):
            if subplot.convert:
                subplot.ax.set_ylabel(f"Z [{self.run.normalisation.R0.units}]")
            else:
                subplot.ax.set_ylabel(f"Z/R0")