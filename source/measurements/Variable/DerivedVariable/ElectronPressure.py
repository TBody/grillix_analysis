from source import np
from . import DerivedVariable
from ..BaseVariable import ElectronTemperature, Density

class ElectronPressure(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electron pressure"
        self.electron_temperature = ElectronTemperature()
        self.density = Density()
        self.base_variables = [self.electron_temperature, self.density]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.Te0*self.normalisation.n0).to('kilopascal')

    def fetch_values(self, **kwargs):
        
        electron_pressure = self.dimensional_array(self.electron_temperature(**kwargs)) * self.dimensional_array(self.density(**kwargs))

        return self.normalised_ScalarArray(electron_pressure)
