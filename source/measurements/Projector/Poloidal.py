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