from source.Variable.dynamic_base import BaseVariable

class ElectronTemperature(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('logte', **kwargs)
        self.title = "Electron temp."
        
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Te0
        
