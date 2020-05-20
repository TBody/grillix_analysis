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
    
    def values(self, **kwargs):
        
        output = self.sound_speed(**kwargs)**2/self.alfven_speed(**kwargs)**2
        
        return self.check_units(output)
    
    