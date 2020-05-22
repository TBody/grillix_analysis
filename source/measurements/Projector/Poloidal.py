from source import np, mplcolors
from . import Projector
from ..Operator import ReduceToPoloidal

class Poloidal(Projector):
    
    def __init__(self, reduction, run=None):
        super().__init__(reduction=reduction, run=run)

    def set_run(self):
        
        self.grid = self.run.grid
        if self.grid.SI_units:
            self.x = self.grid.x_unique.magnitude
            self.y = self.grid.y_unique.magnitude
        else:
            self.x = self.grid.x_unique
            self.y = self.grid.y_unique

    def request_reduction(self, reduction):
        return reduction.cast_to_subclass(ReduceToPoloidal)

    # def slice_z(self, variable):
    #     # If setting time_slice, toroidal_slice, or poloidal_slice, must pass as keyword arguments
        
    #     z_unstructured = variable(self.time_slice, self.toroidal_slice, self.poloidal_slice)
        
    #     return z_unstructured
    
    # def structure_z(self, z_unstructured):
        
    #     z_reduced = np.squeeze(self.reduction(z_unstructured, dimension_to_keep=self.dimension_to_keep))

    #     z_structured = self.grid.vector_to_matrix(z_reduced)
        
    #     return z_structured
    
# 
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