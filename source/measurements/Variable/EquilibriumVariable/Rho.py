from source import Quantity, np
from . import EquilibriumVariable, Psi
from ...WrappedArray import ScalarArray, VectorArray

class Rho(EquilibriumVariable):

    def __init__(self, run=None):
        self.psi = Psi(run=run)
        super().__init__(title="Norm. poloidal Flux", run=run)

    def set_run(self):
        self.psi.run = self.run

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):
        
        psi = self.dimensional_array(self.psi(poloidal_slice))

        # Make values which would give rho < 0 return rho = 0
        psi[np.asarray(psi > self.equi.psiO).nonzero()] = self.equi.psiO

        return ScalarArray(np.sqrt((psi - self.equi.psiO)/(self.equi.psiX - self.equi.psiO)))

    def values_finalize(self, values, units):
        
        return values, units