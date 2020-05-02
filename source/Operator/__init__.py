from source import np
class Operator:

    def __init__(self, run=None):
        if run != None:
            self.set_run(run)
    
    def set_run(self, run):
        self.run = run
        self.normalisation = run.normalisation
        if hasattr(self, "set_normalisation_factor"):
            self.set_normalisation_factor()
        
        if hasattr(self, "set_values_from_run"):
            self.set_values_from_run()

    def __call__(self, z):
        pass
    
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