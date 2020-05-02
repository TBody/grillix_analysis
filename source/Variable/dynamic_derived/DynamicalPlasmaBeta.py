from source.Variable.dynamic_derived import DerivedDynamicVariable, np
from .AlfvenSpeed import AlfvenSpeed
from .SoundSpeed import SoundSpeed

class DynamicalPlasmaBeta(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.title = "Local Beta_e"

    def set_values_from_run(self):
        self.alfven_speed = AlfvenSpeed(run=self.run)
        self.sound_speed = SoundSpeed(run=self.run)

    def set_normalisation_factor(self):
        self.normalisation_factor =  self.normalisation.beta_0

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):

        return (self.sound_speed(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)**2
              /self.alfven_speed(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)**2)