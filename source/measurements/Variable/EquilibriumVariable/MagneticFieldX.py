from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldX(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(run=run)
        title = "B x"

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.equi.Bx_grid_vector[poloidal_slice]

    def value(self, x, y):
        return self.equi.Bx_func(x,y)