from source import np, unit_registry
from . import DerivedVariable
from ..BaseVariable import Density, ParallelIonVelocity, ParallelCurrent
from ..EquilibriumVariable import MagneticFieldAbs

class ParallelElectronVelocity(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "Electron Velocity"
        self.density = Density(**kwargs)
        self.ion_velocity = ParallelIonVelocity(**kwargs)
        self.current = ParallelCurrent(**kwargs)

        self.base_variables = [self.density, self.ion_velocity, self.current]
        self.display_linear = True
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')
        self._ion_charge = self.normalisation.Z
    
    @property
    def ion_charge(self):
        if self.convert:
            return self._ion_charge
        else:
            return self._ion_charge.magnitude

    def values(self, **kwargs):
        
        output = self.ion_velocity(**kwargs) - self.current(**kwargs)/(self.ion_charge * self.density(**kwargs))

        return self.check_units(output)
