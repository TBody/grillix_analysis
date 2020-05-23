from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldPitch(EquilibriumVariable):

    def __init__(self, run=None):
        super().__init__(title="Field pitch", run=run)

    @property
    def normalisation_factor(self):
        return self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        Bpol = self.equi.Bpol(poloidal_slice=poloidal_slice)
        Babs = self.equi.Babs(poloidal_slice=poloidal_slice)

        return Bpol.vector_magnitude/Babs

    def value(self, x, y):

        Bpol = self.equi.Bpol.value(x,y)
        Babs = self.equi.Babs.value(x,y)

        return Bpol.vector_magnitude/Babs