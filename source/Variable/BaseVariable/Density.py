from source import Quantity
from source.Variable.BaseVariable import BaseVariable

class Density(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('logne', **kwargs)
        self.title = "Density"

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.n0
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        if isinstance(value, Quantity):
            return f"{value.to_base_units():6.4g}"
        else:
            return f"{value:6.4g}"