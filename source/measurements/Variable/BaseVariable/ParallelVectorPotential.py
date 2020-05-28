from . import BaseVariable

class ParallelVectorPotential(BaseVariable):
    
    def __init__(self, run=None):
        self.parallel_scalar = True
        super().__init__('aparx', "Vector Potential", run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.beta_0 * self.normalisation.B0 * self.normalisation.rho_s0
        
