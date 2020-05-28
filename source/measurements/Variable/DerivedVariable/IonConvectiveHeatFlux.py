from source import np
from ...WrappedArray import VectorArray
from . import DerivedVariable, TotalVelocity
from ..BaseVariable import Density, IonTemperature

class IonConvectiveHeatFlux(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Ion convective heat flux"
        self.vector_variable = True
        self.density = Density()
        self.ion_temperature = IonTemperature()
        self.total_velocity = TotalVelocity()
        
        self.base_variables = [self.density, self.ion_temperature, self.total_velocity]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.n0 * self.normalisation.c_s0 *self.normalisation.Ti0).to('W / m**2')

    def fetch_values(self, **kwargs):
        
        density = self.dimensional_array(self.density(**kwargs))
        ion_temperature = self.dimensional_array(self.ion_temperature(**kwargs))
        total_velocity = self.dimensional_array(self.total_velocity(**kwargs))

        ion_convective_flux = density[..., np.newaxis] * ion_temperature[..., np.newaxis] * total_velocity

        return self.normalised_VectorArray(ion_convective_flux)
        
