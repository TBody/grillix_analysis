from source.Variable.dynamic_derived import DerivedDynamicVariable, SoundSpeed
from source.Variable.dynamic_base import Density

class SaturationCurrent(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.density = Density(**kwargs)
        self.sound_speed = SoundSpeed(**kwargs)
        
        self.title = "Saturation current"

        self.check_base_variables([self.density, self.sound_speed])
    
    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.electron_charge * self.density.normalisation_factor * self.sound_speed.normalisation_factor
        self.normalisation_factor =  self.normalisation_factor.to('kiloamperes/meter**2')

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):

        return 0.5*self.density(time_slice, toroidal_slice, poloidal_slice)*self.sound_speed(time_slice, toroidal_slice, poloidal_slice)