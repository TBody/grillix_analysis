from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class MagneticFieldAbs(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="magnitude(B)", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):

        return ScalarArray(
            np.sqrt(self.equi.Bx_grid_vector[poloidal_slice]**2 + self.equi.By_grid_vector[poloidal_slice]**2 + self.equi.Btor_grid_vector[poloidal_slice]**2)
        ) 
