from source import np
class Operator:

    def __init__(self, run=None):
        self.run = run
    
    from source.shared.properties import (update_run_values, update_normalisation_factor, run, convert)
    
    def __call__(self, z):
        return NotImplemented
    
    def find_neighbouring_plane(self, z, reverse=False):
       
        if not(reverse):
            # Find the plane in the direction of the toroidal field
            return np.roll(z, shift=-1, axis=1)
        else:
            # Find the plane in the direction against the toroidal field
            return np.roll(z, shift=+1, axis=1)

from .ToroidalReduction import ToroidalReduction
from .TimeReduction     import TimeReduction
from .PadToGrid         import PadToGrid
from .ParallelGradient  import ParallelGradient