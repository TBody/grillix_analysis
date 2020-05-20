from source import np
from . import DerivedVariable
from ..BaseVariable import ElectronTemperature

class SoundSpeed(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Local sound speed"
        self.electron_temperature = ElectronTemperature(run=run)
        self.base_variables = [self.electron_temperature]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')
        self._Mi = self.normalisation.Mi
    
    @property
    def Mi(self):
        if self.SI_units:
            return self._Mi
        else:
            return 1.0

    def values(self, **kwargs):

        output = np.sqrt(self.electron_temperature(**kwargs)/self.Mi)

        return self.check_units(output)
