from source import np, unit_registry
from . import DerivedVariable
from ..BaseVariable import Density
from ..EquilibriumVariable import MagneticFieldAbs

class AlfvenSpeed(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Local Alfven speed"
        self.density = Density()
        self.magnetic_field_strength = MagneticFieldAbs()

        self.base_variables = [self.density, self.magnetic_field_strength]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        # The normalisation factor for Alfven speed is v_A0. However, we want to be able to compare to
        # velocities like the sound speed and u_par. As such, we use c_s0 as the normalisation factor
        return self.normalisation.c_s0.to('kilometers/second')
    
    @property
    def Mi(self):
        return self.normalisation.Mi
    
    @property
    def vacuum_permeability(self):
        return self.normalisation.vacuum_permeability

    def fetch_values(self, **kwargs):

        magnetic_field_strength = self.dimensional_array(self.magnetic_field_strength(**kwargs))
        density = self.dimensional_array(self.density(**kwargs))
        
        alfven_speed = magnetic_field_strength / np.sqrt(density * self.vacuum_permeability * self.Mi)

        return self.normalised_ScalarArray(alfven_speed)

