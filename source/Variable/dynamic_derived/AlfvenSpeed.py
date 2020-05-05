from source import np, unit_registry
from source.Variable.dynamic_derived import DerivedDynamicVariable
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
        return self.calculate_values(self.magnetic_field_strength.values(**kwargs), self.density.values(**kwargs))
    
    @staticmethod
    @unit_registry.wraps(None, (None, None))
    def calculate_values(magnetic_field_strength, density):
        return magnetic_field_strength/np.sqrt(density)