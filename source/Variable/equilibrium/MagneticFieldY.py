from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldY(EquilibriumVariable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "B y"

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.equi.By_grid_vector[poloidal_slice]

    def value(self, x, y):
        return self.equi.By_func(x,y)