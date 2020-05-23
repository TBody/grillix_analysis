from source import np
from .. import MComponent

class Projector(MComponent):

    def __init__(self, run=None):
        super().__init__(run)
    
    def request_reduction(self, reduction):
        # projectors require a specific data shape, i.e. only poloidal points, no dimensions corresponding to 
        # time or toroidal values. To eliminate these extra dimensions, a reduction is used.
        # The user may supply a generic reduction (which will have a specific reduction function, i.e. np.mean).
        # This function converts it into a subclass, which uses the reduction function to cast the data into the 
        # correct shape
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented request_reduction")

    def determine_slices(self, **kwargs):
        # This function must take keyword arguments for slicing, and return time_slice, poloidal_slice, and
        # poloidal_slices
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented determine_slices")

    def shape_values(self, values):
        # This function should cast the array values into a shape such that it can be plotted as
        # plot(projector.x, values) for 1D projectors
        # pcolormesh(projector.x, projector.y, values) for 2D projectors
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented shape_values")

from .Poloidal import Poloidal