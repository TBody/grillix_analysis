from source import np
from . import Projector
from ..Operator import ReduceToPoloidal

class Poloidal(Projector):
    
    def __init__(self, run=None):
        super().__init__(run=run)

    def request_reduction(self, reduction):
        return reduction.cast_to_subclass(ReduceToPoloidal)

    def set_run(self):
        self.grid = self.run.grid
    
    @property
    def x(self):
        return self.grid.x_unique
    
    @property
    def y(self):
        return self.grid.y_unique

    @property
    def xmin(self):
        return self.grid.xmin

    @property
    def xmax(self):
        return self.grid.xmax

    @property
    def ymin(self):
        return self.grid.ymin

    @property
    def ymax(self):
        return self.grid.ymax

    @property
    def x_normalisation(self):
        return self.grid.spatial_normalisation
    
    @property
    def y_normalisation(self):
        return self.grid.spatial_normalisation

    def determine_slices(self, time_slice=slice(-1, None), toroidal_slice=slice(1), poloidal_slice=slice(None)):
        # Natural slicing
        # Default to use the last snap, the 0th plane, and all poloidal points
        return time_slice, toroidal_slice, poloidal_slice

    def shape_values(self, values):
        # Convert z(l) unstructured vector to z(x, y) structured matrix
        return self.grid.vector_to_matrix(values)

    # def __call__(self, subplot, linestyle='-', linewidth=0.5):
    #     assert(self.initialised), f"Annotate called before supplying Run values"
        
    #     try:
    #         self.run.penalisation_contours[0].plot(subplot.ax, color='r', linestyle=linestyle, linewidth=linewidth)
    #         self.run.penalisation_contours[-1].plot(subplot.ax, color='r', linestyle=linestyle, linewidth=linewidth)
    #     except AttributeError:
    #         print("Run has no penalisation_contours")

    #     try:
    #         self.run.parallel_limit_contours[0].plot(subplot.ax, color='b', linestyle=linestyle, linewidth=linewidth)
    #         self.run.parallel_limit_contours[1].plot(subplot.ax, color='b', linestyle=linestyle, linewidth=linewidth)
    #     except AttributeError:
    #         print("Run has no parallel_limit_contours")

    #     try:
    #         self.run.divertor_polygon.plot(subplot.ax, color='b', linestyle=linestyle, linewidth=linewidth)
    #     except AttributeError:
    #         print("Run has no divertor_polygon")
    #     try:
    #         self.run.exclusion_polygon.plot(subplot.ax, color='g', linestyle=linestyle, linewidth=linewidth)
    #     except AttributeError:
    #         print("Run has no exclusion_polygon")
        
    #     try:
    #         self.run.seperatrix[0].plot(subplot.ax, color='g', linestyle=linestyle, linewidth=linewidth)
    #     except AttributeError:
    #         print("Run has no seperatrix")

    #     subplot.ax.set_xlim(left=self.run.grid.xmin, right=self.run.grid.xmax)
    #     subplot.ax.set_ylim(bottom=self.run.grid.ymin, top=self.run.grid.ymax)
        
    # def label_axes(self, subplot):
    #     if not(subplot.hide_xlabel):
    #         if subplot.SI_units:
    #             subplot.ax.set_xlabel(f"R [{self.run.normalisation.R0.units}]")
    #         else:
    #             subplot.ax.set_xlabel(f"R/R0")
            
    #     if not(subplot.hide_ylabel):
    #         if subplot.SI_units:
    #             subplot.ax.set_ylabel(f"Z [{self.run.normalisation.R0.units}]")
    #         else:
    #             subplot.ax.set_ylabel(f"Z/R0")