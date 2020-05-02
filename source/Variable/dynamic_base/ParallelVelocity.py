from source.Variable.dynamic_base import BaseVariable

class ParallelVelocity(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('uparx', **kwargs)
        self.title = "Velocity"
        self.display_linear      = True
        
    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.c_s0.to('kilometers/second')
        
