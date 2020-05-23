from source import Quantity, np
from ...WrappedArray import ScalarArray, VectorArray
from . import EquilibriumVariable

class RadialUnitVector(EquilibriumVariable):
    # Unit vector across the flux surface
    def __init__(self, run=None):
        self.vector_variable = True
        super().__init__(title="Radial unit vector", run=run)

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        Bx = self.equi.Bx_grid_vector[poloidal_slice]
        By = self.equi.By_grid_vector[poloidal_slice]
        Bpol = np.sqrt(Bx**2 + By**2)

        return VectorArray.poloidal(R_array = -By/Bpol, Z_array = Bx/Bpol)

    def value(self, x, y):
        Bx = self.equi.Bx_func(x,y)
        By = self.equi.By_func(x,y)
        Bpol = np.sqrt(Bx**2 + By**2)

        return VectorArray.poloidal(R_array = -By/Bpol, Z_array = Bx/Bpol)