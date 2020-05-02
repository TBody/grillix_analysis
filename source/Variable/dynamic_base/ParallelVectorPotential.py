from source.Variable.dynamic_base import BaseVariable

class ParallelVectorPotential(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('aparx', **kwargs)
        self.title = "Vector Potential"
        
    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.beta_0 * self.normalisation.B0 * self.normalisation.rho_s0
        
