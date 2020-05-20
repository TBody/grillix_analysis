from . import DerivedVariable, SoundSpeed
from ..BaseVariable import Density

class SaturationCurrent(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "Saturation current"
        self.density = Density(**kwargs)
        self.sound_speed = SoundSpeed(**kwargs)

        self.base_variables = [self.density, self.sound_speed]
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.electron_charge * self.density.normalisation_factor * self.sound_speed.normalisation_factor
        self.normalisation_factor = self.normalisation_factor.to('kiloamperes/meter**2')
    
    @property
    def e(self):
        if self.convert:
            return self.normalisation.electron_charge
        else:
            return 1.0

    def values(self, **kwargs):
        
        return self.check_units(0.5 * self.e * self.density(**kwargs) * self.sound_speed(**kwargs))