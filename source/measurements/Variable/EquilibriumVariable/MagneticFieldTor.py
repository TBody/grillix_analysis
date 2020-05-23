from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldTor(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="B toroidal", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.equi.Btor_grid_vector[poloidal_slice]

    def value(self, x, y):
        return self.equi.Btor_func(x,y)