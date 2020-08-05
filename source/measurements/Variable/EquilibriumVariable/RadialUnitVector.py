from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class RadialUnitVector(EquilibriumVariable):
    # Unit vector across the flux surface
    def __init__(self, run=None):
        self.vector_variable = True
        super().__init__(title="Radial unit vector", run=run)

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):

        helicity = getattr(self.equi, "helicity", 1.0)

        Bx = helicity * self.equi.Bx_grid_vector[poloidal_slice]
        By = helicity * self.equi.By_grid_vector[poloidal_slice]
        Bpol = np.sqrt(Bx**2 + By**2)

        return VectorArray.poloidal(R_array = -By/Bpol, Z_array = Bx/Bpol)
