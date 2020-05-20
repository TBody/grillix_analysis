from . import BaseVariable

class ScalarPotential(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('potxx', "Potential", run=run)
        
    @property
    def normalisation_factor(self):
        return (self.normalisation.Te0/self.normalisation.electron_charge).to("kilovolt")
        