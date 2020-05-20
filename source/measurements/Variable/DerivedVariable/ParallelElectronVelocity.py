from source import np, unit_registry
from . import DerivedVariable
from ..BaseVariable import Density, ParallelIonVelocity, ParallelCurrent
from ..EquilibriumVariable import MagneticFieldAbs

class ParallelElectronVelocity(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electron Velocity"
        self.density = Density(run=run)
        self.ion_velocity = ParallelIonVelocity(run=run)
        self.current = ParallelCurrent(run=run)

        self.base_variables = [self.density, self.ion_velocity, self.current]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')
        self._ion_charge = self.normalisation.Z
    
    @property
    def ion_charge(self):
        if self.SI_units:
            return self._ion_charge
        else:
            return self._ion_charge.magnitude

    def values(self, **kwargs):
        
        output = self.ion_velocity(**kwargs) - self.current(**kwargs)/(self.ion_charge * self.density(**kwargs))

        return self.check_units(output)
