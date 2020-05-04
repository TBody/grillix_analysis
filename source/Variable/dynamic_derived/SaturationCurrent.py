from source.Variable.dynamic_derived import DerivedDynamicVariable, SoundSpeed
from source.Variable.dynamic_base import Density

class SaturationCurrent(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "Saturation current"
        self.density = Density(**kwargs)
        self.sound_speed = SoundSpeed(**kwargs)
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.electron_charge * self.density.normalisation_factor * self.sound_speed.normalisation_factor
        self.normalisation_factor = self.normalisation_factor.to('kiloamperes/meter**2')

    def update_run_values(self):
        self.check_base_variables([self.density, self.sound_speed])

    def values(self, **kwargs):
        
        return 0.5*self.density.values(**kwargs)*self.sound_speed.values(**kwargs)