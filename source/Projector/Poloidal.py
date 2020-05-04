from source import np, mplcolors
from . import Projector
from .PoloidalAnnotate import PoloidalAnnotate

class Poloidal(Projector):
    
    annotate = PoloidalAnnotate()

    def __init__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None), **kwargs):
        super().__init__(**kwargs)

        self.time_slice = time_slice
        self.toroidal_slice = toroidal_slice
        self.poloidal_slice = poloidal_slice
    
    def update_run_values(self):
        
        self.grid = self.run.grid
        if self.grid.convert:
            self.x = self.grid.x_unique.magnitude
            self.y = self.grid.y_unique.magnitude
        else:
            self.x = self.grid.x_unique
            self.y = self.grid.y_unique

        self.annotate.run = self.run
    
    def slice_and_structure(self, variable):
        # If setting time_slice, toroidal_slice, or poloidal_slice, must pass as keyword arguments
        
        z_unstructured = variable(self.time_slice, self.toroidal_slice, self.poloidal_slice)
        
        return self.grid.vector_to_matrix(z_unstructured)
    
