from source import np, Quantity, Dimensionless
from ...WrappedArray import VectorArray
from . import DerivedVariable
from ..BaseVariable import IonTemperature
from source.measurements.Operator import ParallelGradient, VectorParallel

class IonConductiveHeatFlux(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Ion Conductive heat flux"
        self.vector_variable = True
        self.ion_temperature = IonTemperature()
        self.vector_parallel = VectorParallel()
        self.parallel_gradient = ParallelGradient()
        
        self.base_variables = [self.ion_temperature, self.vector_parallel, self.parallel_gradient]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.n0 * self.normalisation.c_s0 *self.normalisation.Ti0).to('W / m**2')
    
    @property
    def chipar_i(self):
        return self.normalisation.chipar_i

    def fetch_values(self, **kwargs):
        # The unit conversion is unclear. However, the normalised conductive heat flux and the normalised 
        # convective heat flux should have the same units. Calculate normalised, and then
        # use the convective normalisation factor

        ion_temperature, _ = self.ion_temperature(**kwargs)
        ion_temperature_gradient, _ = self.parallel_gradient(ion_temperature, Dimensionless)
        ion_conductive_flux = -self.chipar_i * ion_temperature**2.5 * ion_temperature_gradient
        
        ion_conductive_flux, _ = self.vector_parallel(ion_conductive_flux, Dimensionless)

        return VectorArray(ion_conductive_flux)
        
