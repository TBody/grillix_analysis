from . import BaseVariable

class ParallelIonVelocity(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('uparx', 'Ion Velocity', run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')
