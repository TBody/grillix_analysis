from source.Variable.dynamic_derived import DerivedDynamicVariable, np
from source.Variable.dynamic_base import Density

class AlfvenSpeed(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.density = Density(**kwargs)
        
        self.display_linear      = True
        
        self.title = "Local Alfven speed"

        self.check_base_variables([self.density])

    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.v_A0
        self.normalisation_factor =  self.normalisation_factor.to('kilometers/second')
    
    def set_values_from_run(self):
        self.magnetic_field_strength = self.run.equilibrium.Babs

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):

        return self.magnetic_field_strength(time_slice, toroidal_slice, poloidal_slice)/np.sqrt(self.density(time_slice, toroidal_slice, poloidal_slice))