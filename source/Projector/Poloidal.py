from source import np, mplcolors
from . import Projector
from .PoloidalAnnotate import PoloidalAnnotate
from source.shared import QArray

class Poloidal(Projector):
    
    annotate = PoloidalAnnotate()

    def __init__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None), **kwargs):
        super().__init__(**kwargs)

        self.time_slice = time_slice
        self.toroidal_slice = toroidal_slice
        self.poloidal_slice = poloidal_slice
    
    def set_values_from_run(self):
        self.grid = self.run.grid
        self.x = self.grid.x_unique
        self.y = self.grid.y_unique

        self.annotate.set_run(self.run, self)
    
    def slice_and_structure(self, variable):
        # If setting time_slice, toroidal_slice, or poloidal_slice, must pass as keyword arguments
        
        z_unstructured = variable(self.time_slice, self.toroidal_slice, self.poloidal_slice)
        assert(isinstance(z_unstructured, QArray))
        
        return self.grid.vector_to_matrix(z_unstructured)
    
