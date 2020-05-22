from source import np, Quantity
from .. import MComponent, WrappedArray

class Operator(MComponent):

    def __init__(self, run=None):
        super().__init__(run)

    def __call__(self, values, units):
        raise NotImplementedError(f"Prototype for __call__ should be overwritten by {self.__class__.__name__}")
        
    def operate_on_values(self, values, units):
        
        values.check_dimensions()
        [values, units] = self.__call__(values, units)
        values.check_dimensions()

        # Check that the returned objects are of the correct types
        assert(isinstance(values, WrappedArray))
        assert(isinstance(units, Quantity))

        return values, units
    
    def find_neighbouring_plane(self, values, reverse=False):
       
        if not(reverse):
            # Find the plane in the direction of the toroidal field
            return np.roll(values, shift=-1, axis=1)
        else:
            # Find the plane in the direction against the toroidal field
            return np.roll(values, shift=+1, axis=1)

from .PadToGrid         import PadToGrid
# from .ParallelGradient  import ParallelGradient
from .PerpendicularGradient  import PerpendicularGradient
from .VectorAbsolute import VectorAbsolute
from .VectorRadialProjection import VectorRadialProjection
from .VectorPoloidalProjection import VectorPoloidalProjection

from .Reduction import *