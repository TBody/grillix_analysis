from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldPitch(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="Field pitch", run=run)

    def fetch_values(self, poloidal_slice=slice(None), **kwargs):
        
        Bpol = self.dimensional_array(self.equi.Bpol(poloidal_slice=poloidal_slice))
        Babs = self.dimensional_array(self.equi.Babs(poloidal_slice=poloidal_slice))
        
        return self.normalised_ScalarArray(Bpol.vector_magnitude/Babs)

    def values_finalize(self, values, units):
        
        return values, units