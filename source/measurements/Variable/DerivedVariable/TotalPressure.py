from source import np
from . import DerivedVariable
from ..BaseVariable import ElectronTemperature, Density, IonTemperature

class TotalPressure(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "Total pressure"
        self.electron_temperature = ElectronTemperature(**kwargs)
        self.ion_temperature = IonTemperature(**kwargs)
        self.density = Density(**kwargs)
        self.base_variables = [self.electron_temperature, self.density, self.ion_temperature]

        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = ((self.normalisation.Te0 + self.normalisation.Ti0)*self.normalisation.n0).to('kilopascal')

    def values(self, **kwargs):

        output = (self.electron_temperature(**kwargs) + self.ion_temperature(**kwargs))*self.density(**kwargs)

        return self.check_units(output)
