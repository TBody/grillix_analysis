from source import Quantity
from . import BaseVariable

class Density(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('logne', 'Density', run)

    @property
    def normalisation_factor(self):
        return self.normalisation.n0
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        if isinstance(value, Quantity):
            return f"{value.to_base_units():6.4g}"
        else:
            return f"{value:6.4g}"