from source.Variable.dynamic_derived import DerivedDynamicVariable, np
from source.Variable.dynamic_base import ElectronTemperature

class SoundSpeed(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "Local sound speed"
        self.electron_temperature = ElectronTemperature(**kwargs)
        self.display_linear = True
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = np.sqrt(self.normalisation.Te0/self.normalisation.Mi)
        self.normalisation_factor = self.normalisation_factor.to('kilometers/second')

    def update_run_values(self):
        self.check_base_variables([self.electron_temperature])

    def values(self, **kwargs):

        return np.sqrt(self.electron_temperature.values(**kwargs))