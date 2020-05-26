from source import np
from . import DerivedVariable
from ..BaseVariable import Density, IonTemperature

class IonPressure(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Ion pressure"
        self.ion_temperature = IonTemperature()
        self.density = Density()
        self.base_variables = [self.density, self.ion_temperature]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.Ti0*self.normalisation.n0).to('kilopascal')

    def fetch_values(self, **kwargs):
        
        ionpressure = self.dimensional_array(self.ion_temperature(**kwargs)) * self.dimensional_array(self.density(**kwargs))

        return self.normalised_ScalarArray(ionpressure)
