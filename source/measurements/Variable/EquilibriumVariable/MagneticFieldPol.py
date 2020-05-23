from source import Quantity, np
from ...WrappedArray import VectorArray
from . import EquilibriumVariable

class MagneticFieldPol(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="B poloidal", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        return VectorArray.poloidal_vector(
            R_array=self.equi.Bx_grid_vector[poloidal_slice],
            Z_array=self.equi.By_grid_vector[poloidal_slice])

    def value(self, x, y):

        return VectorArray.poloidal_vector(
            R_array=self.equi.Bx_func(x,y),
            Z_array=self.equi.By_func(x,y))