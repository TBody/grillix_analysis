from source import np
from source.Variable.dynamic_derived import DerivedDynamicVariable
from source.Variable.dynamic_base import ElectronTemperature

class SoundSpeed(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "Local sound speed"
        self.electron_temperature = ElectronTemperature(**kwargs)
        self.display_linear = True
        self.base_variables = [self.electron_temperature]

        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')
        self._Mi = self.normalisation.Mi
    
    @property
    def Mi(self):
        if self.convert:
            return self._Mi
        else:
            return 1.0

    def values(self, **kwargs):

        output = np.sqrt(self.electron_temperature(**kwargs)/self.Mi)

        return self.check_units(output)
