from source import Quantity, np
from ...Result import VectorResult
from . import EquilibriumVariable

class MagneticFieldAbs(EquilibriumVariable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "magnitude(B)"

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        values = np.sqrt(self.equi.Bx_grid_vector[poloidal_slice]**2 + self.equi.By_grid_vector[poloidal_slice]**2 + self.equi.Btor_grid_vector[poloidal_slice]**2)
        return values

    def value(self, x, y):
        return np.sqrt(self.equi.Bx_func(x,y)**2 + self.equi.By_func(x,y)**2 + self.equi.Btor_func(x,y)**2)