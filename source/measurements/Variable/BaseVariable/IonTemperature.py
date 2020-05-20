from . import BaseVariable

class IonTemperature(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('logti', 'Ion temp.', run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.Ti0
        