from source import np, unit_registry
from . import DerivedVariable
from ..BaseVariable import Density, ParallelIonVelocity, ParallelCurrent
from ..EquilibriumVariable import MagneticFieldAbs

class ParallelElectronVelocity(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electron Velocity"
        self.density = Density()
        self.ion_velocity = ParallelIonVelocity()
        self.current = ParallelCurrent()

        self.base_variables = [self.density, self.ion_velocity, self.current]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')

    def fetch_values(self, **kwargs):
        ion_velocity = self.dimensional_array(self.ion_velocity(**kwargs))
        current = self.dimensional_array(self.current(**kwargs))
        density = self.dimensional_array(self.density(**kwargs))

        electron_velocity = ion_velocity - current/(self.normalisation.Z * density)

        return self.normalised_ScalarArray(electron_velocity)
