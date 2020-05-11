from source.Variable.DerivedVariable import DerivedVariable
from .AlfvenSpeed import AlfvenSpeed
from .SoundSpeed import SoundSpeed

class DynamicalPlasmaBeta(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "Local Beta_e"
        self.alfven_speed = AlfvenSpeed(**kwargs)
        self.sound_speed = SoundSpeed(**kwargs)
        self.base_variables = [self.sound_speed, self.alfven_speed]
        
        super().__init__(**kwargs)
    
    def values(self, **kwargs):
        
        output = self.sound_speed(**kwargs)**2/self.alfven_speed(**kwargs)**2
        
        return self.check_units(output)
    
    