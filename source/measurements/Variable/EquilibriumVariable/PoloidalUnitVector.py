from source import Quantity, np
from ...Result import VectorResult
from . import EquilibriumVariable

class PoloidalUnitVector(EquilibriumVariable):
    # Unit vector along the flux surface
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vector_variable = True

        self.title = "Poloidal unit vector"

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        Bx = self.equi.Bx_grid_vector[poloidal_slice]
        By = self.equi.By_grid_vector[poloidal_slice]
        Bpol = np.sqrt(Bx**2 + By**2)

        return VectorResult.poloidal_vector_from_subarrays(R_array = Bx/Bpol, Z_array = By/Bpol)

    def value(self, x, y):
        Bx = self.equi.Bx_func(x,y)
        By = self.equi.By_func(x,y)
        Bpol = np.sqrt(Bx**2 + By**2)

        return VectorResult.poloidal_vector_from_subarrays(R_array = Bx/Bpol, Z_array = By/Bpol)
