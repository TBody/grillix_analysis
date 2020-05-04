from source.Variable.dynamic_derived import DerivedDynamicVariable, np
from source.Variable.dynamic_base import Density

class AlfvenSpeed(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.density = Density(**kwargs)
        self.display_linear      = True
        self.title = "Local Alfven speed"
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.v_A0
        self.normalisation_factor = self.normalisation_factor.to('kilometers/second')
    
    def update_run_values(self):
        self.check_base_variables([self.density])
        self.magnetic_field_strength = self.run.equilibrium.Babs

    def values(self, **kwargs):
        return self.magnetic_field_strength.values(**kwargs)/np.sqrt(self.density.values(**kwargs))