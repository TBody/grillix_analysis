from source import np, Quantity, Dimensionless
from ...WrappedArray import VectorArray
from . import DerivedVariable
from ..BaseVariable import ElectronTemperature
from source.measurements.Operator import ParallelGradient, VectorParallel

class ElectronConductiveHeatFlux(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electron Conductive heat flux"
        self.vector_variable = True
        self.electron_temperature = ElectronTemperature()
        self.vector_parallel = VectorParallel()
        self.parallel_gradient = ParallelGradient()
        
        self.base_variables = [self.electron_temperature, self.vector_parallel, self.parallel_gradient]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.n0 * self.normalisation.c_s0 *self.normalisation.Ti0).to('W / m**2')
    
    @property
    def chipar_e(self):
        return (self.normalisation.chipar_e).to('').magnitude

    def fetch_values(self, **kwargs):
        # The unit converselectron is unclear. However, the normalised conductive heat flux and the normalised 
        # convective heat flux should have the same units. Calculate normalised, and then
        # use the convective normalisation factor

        electron_temperature, _ = self.electron_temperature(**kwargs)
        electron_temperature_gradient, _ = self.parallel_gradient(electron_temperature, Dimensionless)
        electron_conductive_flux = -self.chipar_e * electron_temperature**2.5 * electron_temperature_gradient
        
        electron_conductive_flux, _ = self.vector_parallel(electron_conductive_flux, Dimensionless)

        return VectorArray(electron_conductive_flux)
        
