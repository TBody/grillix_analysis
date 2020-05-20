from . import BaseVariable

class ElectronTemperature(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('logte', "Electron temp.", run)
        
    @property
    def normalisation_factor(self):
        return self.normalisation.Te0
        
