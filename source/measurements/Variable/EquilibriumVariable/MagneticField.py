from source import Quantity, np
from ...WrappedArray import VectorArray
from . import EquilibriumVariable

class MagneticField(EquilibriumVariable):

    def __init__(self, run=None):
        self.vector_variable = True
        super().__init__(title="B", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        return VectorArray.cylindrical_vector(
            R_array=self.equi.Bx_grid_vector[poloidal_slice],
            phi_array=self.equi.Btor_grid_vector[poloidal_slice],
            Z_array=self.equi.By_grid_vector[poloidal_slice])

    def value(self, x, y):

        return VectorArray.cylindrical_vector(
            R_array=self.equi.Bx_func(x,y),
            phi_array=self.equi.Btor_func(x,y),
            Z_array=self.equi.By_func(x,y))