from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class PoloidalUnitVector(EquilibriumVariable):
    # Unit vector along the flux surface
    def __init__(self, run=None):
        self.vector_variable = True
        super().__init__(title="Poloidal unit vector", run=run)

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):

        Bx = self.equi.Bx_grid_vector[poloidal_slice]
        By = self.equi.By_grid_vector[poloidal_slice]
        Bpol = np.sqrt(Bx**2 + By**2)

        return VectorArray.poloidal(R_array = Bx/Bpol, Z_array = By/Bpol)
