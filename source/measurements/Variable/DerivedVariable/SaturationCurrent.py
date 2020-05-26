from . import DerivedVariable, SoundSpeed
from ..BaseVariable import Density

class SaturationCurrent(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Saturation current"
        self.density = Density()
        self.sound_speed = SoundSpeed()

        self.base_variables = [self.density, self.sound_speed]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.electron_charge * self.density.normalisation_factor * self.sound_speed.normalisation_factor).to('kiloamperes/meter**2')
    
    @property
    def e(self):
        return self.normalisation.electron_charge

    def fetch_values(self, **kwargs):
        density = self.dimensional_array(self.density(**kwargs))
        sound_speed = self.dimensional_array(self.sound_speed(**kwargs))

        return self.normalised_ScalarArray(0.5 * self.e * density * sound_speed)