from source import Quantity, np
from . import EquilibriumVariable, Psi

class Rho(EquilibriumVariable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Norm. poloidal Flux"
        self.psi = Psi(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = Quantity(1, '')

    def update_run_values(self):
        self.update_base_variables([self.psi])

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        psi = self.psi(poloidal_slice)

        # Make values which would give rho < 0 return rho = 0
        psi[np.asarray(psi > self.equi.psiO).nonzero()] = self.equi.psiO

        return np.sqrt((psi - self.equi.psiO)/(self.equi.psiX - self.equi.psiO))

    def value(self, x, y):
        return self.equi.psi_func(x,y)