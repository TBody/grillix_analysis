from source import np
from .Annotate import Annotate

class Projector:

    annotate = Annotate()

    def __init__(self, reduction, run=None):
        self.reduction = reduction
        self.run = run
    
    from source.shared.properties import (update_run_values, update_normalisation_factor, run, SI_units)

    def slice_and_structure(self, variable):
        return NotImplemented
    
    def __call__(self, variable, **kwargs):
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