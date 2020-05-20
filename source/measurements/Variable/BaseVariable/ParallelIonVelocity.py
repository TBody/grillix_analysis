from . import BaseVariable

class ParallelIonVelocity(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('uparx', **kwargs)
        self.title = "Ion Velocity"
        self.display_linear = True
        
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')
        
