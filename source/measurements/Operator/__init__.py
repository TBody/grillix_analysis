from source import np, Quantity
from .. import MComponent

class Operator(MComponent):

    def __init__(self, run=None):
        super().__init__(run)
    
    def values(self, z):
        return NotImplemented

    def __call__(self, z, **kwargs):
        
        return self.values(z, **kwargs)
    
    def find_neighbouring_plane(self, z, reverse=False):
       
        if not(reverse):
            # Find the plane in the direction of the toroidal field
            return np.roll(z, shift=-1, axis=1)
        else:
            # Find the plane in the direction against the toroidal field
            return np.roll(z, shift=+1, axis=1)

from .ToroidalReduction import ToroidalReduction
from .TimeReduction     import TimeReduction
from .PoloidalReduction import PoloidalReduction
from .PadToGrid         import PadToGrid
# from .ParallelGradient  import ParallelGradient
from .PerpendicularGradient  import PerpendicularGradient
from .AllReduction import AllReduction
from .VectorAbsolute import VectorAbsolute
from .VectorRadialProjection import VectorRadialProjection
from .VectorPoloidalProjection import VectorPoloidalProjection