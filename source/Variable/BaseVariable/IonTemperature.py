from source.Variable.BaseVariable import BaseVariable

class IonTemperature(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('logti', **kwargs)
        self.title = "Ion temp."
        
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Ti0
        