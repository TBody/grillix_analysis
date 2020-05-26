from source import np
from . import DerivedVariable, ElectronPressure, IonPressure

class TotalPressure(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Total pressure"
        self.electron_pressure = ElectronPressure()
        self.ion_pressure = IonPressure()
        self.base_variables = [self.electron_pressure, self.ion_pressure]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return ((self.normalisation.Te0 + self.normalisation.Ti0)*self.normalisation.n0).to('kilopascal')

    def fetch_values(self, **kwargs):
        
        total_pressure = self.dimensional_array(self.electron_pressure(**kwargs)) + self.dimensional_array(self.ion_pressure(**kwargs))

        return self.normalised_ScalarArray(total_pressure)
