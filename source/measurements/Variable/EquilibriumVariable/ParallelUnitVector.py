from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class ParallelUnitVector(EquilibriumVariable):
    # Unit vector along the flux surface
    def __init__(self, run=None):
        self.vector_variable = True
        super().__init__(title="Parallel unit vector", run=run)

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):

        Bx = self.equi.Bx_grid_vector[poloidal_slice]
        By = self.equi.By_grid_vector[poloidal_slice]
        Btor = self.equi.Btor_grid_vector[poloidal_slice]

        Babs = np.sqrt(Bx**2 + By**2 + Btor**2)

        return VectorArray.cylindrical(R_array=Bx/Babs, phi_array=Btor/Babs, Z_array=By/Babs)
