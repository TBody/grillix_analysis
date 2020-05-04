from . import Annotate

class PoloidalAnnotate(Annotate):

    def __init__(self, **kwargs):
        self.initialised = False

    def set_values_from_run(self):
        self.initialised = True

    def __call__(self, subplot, linestyle='-', linewidth=0.5):
        assert(self.initialised), f"Annotate called before supplying Run values"
        
        self.spatial_normalisation = 1 if not(subplot.convert) else self.run.normalisation.R0
        
        self.run.penalisation_contours[0].plot(subplot.ax, self.spatial_normalisation, color='r', linestyle=linestyle, linewidth=linewidth)
        self.run.penalisation_contours[-1].plot(subplot.ax, self.spatial_normalisation, color='r', linestyle=linestyle, linewidth=linewidth)
        
        self.run.divertor_polygon.plot(subplot.ax, self.spatial_normalisation, color='b', linestyle=linestyle, linewidth=linewidth)
        self.run.exclusion_polygon.plot(subplot.ax, self.spatial_normalisation, color='g', linestyle=linestyle, linewidth=linewidth)
        
        self.run.seperatrix[0].plot(subplot.ax, self.spatial_normalisation, color='g', linestyle=linestyle, linewidth=linewidth)
    
    def style_plot(self, subplot):
        self.label_axes(subplot)
        
        # subplot.ax.set_xlim(left=self.projector.grid.xmin, right=self.projector.grid.xmax)
        # subplot.ax.set_ylim(bottom=self.projector.grid.ymin, top=self.projector.grid.ymax)
        
    def label_axes(self, subplot):
        if not(subplot.hide_xlabel):
            if subplot.convert:
                subplot.ax.set_xlabel(f"R [{self.spatial_normalisation.units}]")
            else:
                subplot.ax.set_xlabel(f"R/R0")
            
        if not(subplot.hide_ylabel):
            if subplot.convert:
                subplot.ax.set_ylabel(f"Z [{self.spatial_normalisation.units}]")
            else:
                subplot.ax.set_ylabel(f"Z/R0")