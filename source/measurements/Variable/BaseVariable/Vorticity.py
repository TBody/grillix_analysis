from . import BaseVariable

class Vorticity(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('vortx', "Vorticity", run=run)
        
    @property
    def normalisation_factor(self):
        return (
            self.normalisation.Mi * self.normalisation.n0 * self.normalisation.Te0
            /(self.normalisation.electron_charge * self.normalisation.rho_s0**2 * self.normalisation.B0**2 )
        ).to('coulomb/meter**3')
        
