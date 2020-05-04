from source.Variable.dynamic_base import BaseVariable

class Vorticity(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('vortx', **kwargs)
        self.title = "Vorticity"
        
    def update_normalisation_factor(self):
        self.normalisation_factor = (
            self.normalisation.Mi * self.normalisation.n0 * self.normalisation.Te0
            /(self.normalisation.electron_charge * self.normalisation.rho_s0**2 * self.normalisation.B0**2 )
        ).to('coulomb/meter**3')
        
