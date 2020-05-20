from source import Quantity, np
from ...Result import VectorResult
from . import EquilibriumVariable

class MagneticFieldPol(EquilibriumVariable):

    def __init__(self, **kwargs):
        self.title = "B poloidal"
        self.vector_variable = True

        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        return VectorResult.poloidal_vector_from_subarrays(
            R_array=self.equi.Bx_grid_vector[poloidal_slice],
            Z_array=self.equi.By_grid_vector[poloidal_slice])

    def value(self, x, y):

        return VectorResult.poloidal_vector_from_subarrays(
            R_array=self.equi.Bx_func(x,y),
            Z_array=self.equi.By_func(x,y))