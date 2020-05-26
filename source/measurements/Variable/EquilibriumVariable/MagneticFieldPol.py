from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class MagneticFieldPol(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="B poloidal", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):

        return VectorArray.poloidal(
            R_array=self.equi.Bx_grid_vector[poloidal_slice],
            Z_array=self.equi.By_grid_vector[poloidal_slice]) 
