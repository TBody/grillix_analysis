from source import np
from . import DerivedVariable
from ..BaseVariable import ElectronTemperature

class SoundSpeed(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Local sound speed"
        self.electron_temperature = ElectronTemperature()
        self.base_variables = [self.electron_temperature]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')
    
    @property
    def Mi(self):
        return self.normalisation.Mi

    def fetch_values(self, **kwargs):

        sound_speed = np.sqrt(self.dimensional_array(self.electron_temperature(**kwargs))/self.Mi)

        return self.normalised_ScalarArray(sound_speed)
