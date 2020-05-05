from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldTor(EquilibriumVariable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "B toroidal"

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.equi.Btor_grid_vector[poloidal_slice]

    def value(self, x, y):
        return self.equi.Btor_func(x,y)