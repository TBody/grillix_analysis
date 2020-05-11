from source import np, unit_registry
from source.Variable.DerivedVariable import DerivedVariable
from source.Variable.BaseVariable import Density
from source.Variable.EquilibriumVariable import MagneticFieldAbs

class AlfvenSpeed(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "Local Alfven speed"
        self.density = Density(**kwargs)
        self.magnetic_field_strength = MagneticFieldAbs(**kwargs)

        self.base_variables = [self.density, self.magnetic_field_strength]
        self.display_linear = True
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')

        # The normalisation factor for Alfven speed is v_A0. However, we want to be able to compare to
        # velocities like the sound speed and u_par. As such, we use c_s0 as the normalisation factor
        
        # Term which is needed to convert from SI base variables to velocity units
        self.vA0_to_cs0_SI = (1 / np.sqrt(self.normalisation.vacuum_permeability * self.normalisation.Mi)).to('1/(m ** 0.5 * T * s)')
        # Term which gives the normalisation for the base units
        self.vA0_to_cs0_norm = (self.normalisation.v_A0 / self.normalisation.c_s0).to('')
    
    @property
    def vA0_to_cs0(self):
        if self.convert:
            # Converts from units of T/sqrt(m**3) to m/s
            return self.vA0_to_cs0_SI
        else:
            # Unitless
            return self.vA0_to_cs0_norm

    def values(self, **kwargs):
        
        output = self.magnetic_field_strength(**kwargs)/np.sqrt(self.density(**kwargs)) * self.vA0_to_cs0

        return self.check_units(output)
