from source import np, unit_registry
from . import DerivedVariable
from ..BaseVariable import Density
from ..EquilibriumVariable import MagneticFieldAbs

class AlfvenSpeed(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Local Alfven speed"
        self.density = Density(run=run)
        self.magnetic_field_strength = MagneticFieldAbs(run=run)

        self.base_variables = [self.density, self.magnetic_field_strength]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')
    
    @property
    def vA0_to_cs0(self):
        # The normalisation factor for Alfven speed is v_A0. However, we want to be able to compare to
        # velocities like the sound speed and u_par. As such, we use c_s0 as the normalisation factor
        if self.SI_units:
            # Term which is needed to convert from SI base variables to velocity units
            # Converts from units of T/sqrt(m**3) to m/s
            return (1 / np.sqrt(self.normalisation.vacuum_permeability * self.normalisation.Mi)).to('1/(m ** 0.5 * T * s)')
        else:
            # Term which gives the normalisation for the base units
            # Unitless
            return (self.normalisation.v_A0 / self.normalisation.c_s0).to('')

    def values(self, **kwargs):
        
        output = self.magnetic_field_strength(**kwargs)/np.sqrt(self.density(**kwargs)) * self.vA0_to_cs0

        return self.check_units(output)
