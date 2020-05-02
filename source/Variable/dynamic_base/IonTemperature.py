from source.Variable.dynamic_base import BaseVariable

class IonTemperature(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('logti', **kwargs)
        self.title = "Ion temp."
        
    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.Ti0
        