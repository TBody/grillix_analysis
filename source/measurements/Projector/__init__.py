from source import np
from .. import MComponent

class Projector(MComponent):

    def __init__(self, reduction, run=None):
        self.reduction = reduction
        super().__init__(run)
    
    def slice_and_structure(self, variable):
        return NotImplemented
    
    def __call__(self, variable, run=None):
        # If setting time_slice, toroidal_slice, or poloidal_slice, must pass as keyword arguments

        for key, value in kwargs.items():
            if key in self.__dict__.keys():
                if type(value) is not slice:
                    value = np.atleast_1d(value)
                setattr(self, key, value)
            else:
                raise NotImplementedError(f"No attribute {key} found for Projector {self.__class__.__name__}")
        
        return self.slice_z(variable)
    
    def structure_z(self, z_unstructured):
        
        return NotImplemented

from .Poloidal import Poloidal