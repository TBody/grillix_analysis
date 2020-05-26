from source import Quantity, np
from . import EquilibriumVariable
from ...WrappedArray import ScalarArray, VectorArray

class Psi(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="Poloidal Flux", run=run)

    @property
    def normalisation_factor(self):
        return Quantity(1, 'weber')

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):
        return ScalarArray(self.equi.psi_grid_vector[poloidal_slice])
