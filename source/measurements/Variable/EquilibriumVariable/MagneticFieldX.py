from source import Quantity, np
from . import EquilibriumVariable
from ...WrappedArray import ScalarArray, VectorArray

class MagneticFieldX(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="B x", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):
        return ScalarArray(self.equi.Bx_grid_vector[poloidal_slice]) 
