from source.Variable.dynamic_derived import DerivedDynamicVariable, np
from source.Variable.dynamic_base import ElectronTemperature

class SoundSpeed(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.electron_temperature = ElectronTemperature(**kwargs)
        
        self.display_linear      = True
        
        self.title = "Local sound speed"

        self.check_base_variables([self.electron_temperature])

    def set_normalisation_factor(self):
        self.normalisation_factor =  np.sqrt(self.normalisation.Te0/self.normalisation.Mi)
        self.normalisation_factor =  self.normalisation_factor.to('kilometers/second')

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):

        return np.sqrt(self.electron_temperature(time_slice, toroidal_slice, poloidal_slice))