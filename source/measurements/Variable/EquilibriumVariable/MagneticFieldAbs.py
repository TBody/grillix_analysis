from source import Quantity, np
from ...WrappedArray import VectorArray
from . import EquilibriumVariable

class MagneticFieldAbs(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="magnitude(B)", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        values = np.sqrt(self.equi.Bx_grid_vector[poloidal_slice]**2 + self.equi.By_grid_vector[poloidal_slice]**2 + self.equi.Btor_grid_vector[poloidal_slice]**2)
        return values

    def value(self, x, y):
        return np.sqrt(self.equi.Bx_func(x,y)**2 + self.equi.By_func(x,y)**2 + self.equi.Btor_func(x,y)**2)