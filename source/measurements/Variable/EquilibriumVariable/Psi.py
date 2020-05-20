from source import Quantity, np
from . import EquilibriumVariable

class Psi(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(run=run)
        title = "Poloidal Flux"

    def update_normalisation_factor(self):
        self.normalisation_factor = Quantity(1, 'weber')

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.equi.psi_grid_vector[poloidal_slice]

    def value(self, x, y):
        return self.equi.psi_func(x, y)