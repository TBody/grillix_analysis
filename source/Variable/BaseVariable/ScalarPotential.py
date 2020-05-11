from source.Variable.BaseVariable import BaseVariable

class ScalarPotential(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('potxx', **kwargs)
        self.title = "Potential"
        
    def update_normalisation_factor(self):
        self.normalisation_factor = (self.normalisation.Te0/self.normalisation.electron_charge).to("kilovolt")
        