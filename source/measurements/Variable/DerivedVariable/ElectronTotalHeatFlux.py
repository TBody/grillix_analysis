from source import np
from . import DerivedVariable, ElectronConvectiveHeatFlux, ElectronConductiveHeatFlux

class ElectronTotalHeatFlux(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electron Heat Flux"
        self.vector_variable = True
        self.conductive_flux = ElectronConductiveHeatFlux()
        self.convective_flux = ElectronConvectiveHeatFlux()
        self.base_variables = [self.conductive_flux, self.convective_flux]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.n0 * self.normalisation.c_s0 *self.normalisation.Te0).to('W / m**2')

    def fetch_values(self, **kwargs):
        
        total_heat_flux = self.dimensional_array(self.conductive_flux(**kwargs)) + self.dimensional_array(self.convective_flux(**kwargs))

        return self.normalised_VectorArray(total_heat_flux)
