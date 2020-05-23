from source import Quantity, np
from . import EquilibriumVariable
from ...WrappedArray import ScalarArray, VectorArray

class Psi(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="Poloidal Flux", run=run)

    @property
    def normalisation_factor(self):
        return Quantity(1, 'weber')

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return ScalarArray(self.equi.psi_grid_vector[poloidal_slice])

    def value(self, x, y):
        return ScalarArray(self.equi.psi_func(x, y))