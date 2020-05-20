from . import DerivedVariable, SoundSpeed
from ..BaseVariable import Density

class SaturationCurrent(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Saturation current"
        self.density = Density(run=run)
        self.sound_speed = SoundSpeed(run=run)

        self.base_variables = [self.density, self.sound_speed]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.electron_charge * self.density.normalisation_factor * self.sound_speed.normalisation_factor
        self.normalisation_factor = self.normalisation_factor.to('kiloamperes/meter**2')
    
    @property
    def e(self):
        if self.SI_units:
            return self.normalisation.electron_charge
        else:
            return 1.0

    def values(self, **kwargs):
        
        return self.check_units(0.5 * self.e * self.density(**kwargs) * self.sound_speed(**kwargs))