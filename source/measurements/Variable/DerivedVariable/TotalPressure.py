from source import np
from . import DerivedVariable
from ..BaseVariable import ElectronTemperature, Density, IonTemperature

class TotalPressure(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Total pressure"
        self.electron_temperature = ElectronTemperature(run=run)
        self.ion_temperature = IonTemperature(run=run)
        self.density = Density(run=run)
        self.base_variables = [self.electron_temperature, self.density, self.ion_temperature]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return ((self.normalisation.Te0 + self.normalisation.Ti0)*self.normalisation.n0).to('kilopascal')

    def values(self, **kwargs):

        output = (self.electron_temperature(**kwargs) + self.ion_temperature(**kwargs))*self.density(**kwargs)

        return self.check_units(output)
