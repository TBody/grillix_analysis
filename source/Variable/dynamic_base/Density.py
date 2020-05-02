from source.Variable.dynamic_base import BaseVariable

class Density(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('logne', **kwargs)
        self.title = "Density"

    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.n0
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        
        return f"{value.to_base_units():6.4g}"