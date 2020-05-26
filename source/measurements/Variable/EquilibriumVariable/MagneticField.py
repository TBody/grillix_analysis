from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class MagneticField(EquilibriumVariable):

    def __init__(self, run=None):
        self.vector_variable = True
        super().__init__(title="B", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):

        return VectorArray.cylindrical(
            R_array=self.equi.Bx_grid_vector[poloidal_slice],
            phi_array=self.equi.Btor_grid_vector[poloidal_slice],
            Z_array=self.equi.By_grid_vector[poloidal_slice]) 
