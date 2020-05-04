from source.Variable.dynamic_derived import DerivedDynamicVariable, np
from .AlfvenSpeed import AlfvenSpeed
from .SoundSpeed import SoundSpeed

class DynamicalPlasmaBeta(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "Local Beta_e"
        
        super().__init__(**kwargs)

    def update_run_values(self):
        self.alfven_speed = AlfvenSpeed(run=self.run)
        self.sound_speed = SoundSpeed(run=self.run)
        self.check_base_variables([self.alfven_speed, self.sound_speed])

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.beta_0
    
    def values(self, **kwargs):

        return (self.sound_speed.values(**kwargs)**2/self.alfven_speed.values(**kwargs)**2)