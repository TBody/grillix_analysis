from . import DerivedVariable
from .AlfvenSpeed import AlfvenSpeed
from .SoundSpeed import SoundSpeed

class DynamicalPlasmaBeta(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Local Beta_e"
        self.alfven_speed = AlfvenSpeed(run=run)
        self.sound_speed = SoundSpeed(run=run)
        self.base_variables = [self.sound_speed, self.alfven_speed]
        
        super().__init__(title, run=None)
    
    def fetch_values(self, **kwargs):
        
        sound_speed = self.dimensional_array(self.sound_speed(**kwargs))
        alfven_speed = self.dimensional_array(self.alfven_speed(**kwargs))

        plasma_beta = sound_speed**2 / alfven_speed**2

        return self.normalised_ScalarArray(plasma_beta)
    
    