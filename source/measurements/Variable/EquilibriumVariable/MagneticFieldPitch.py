from source import Quantity, np
from . import EquilibriumVariable

class MagneticFieldPitch(EquilibriumVariable):

    def __init__(self, **kwargs):
        self.title = "Field pitch"

        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        Bpol = self.equi.Bpol(poloidal_slice=poloidal_slice)
        Babs = self.equi.Babs(poloidal_slice=poloidal_slice)

        return Bpol.vector_magnitude/Babs

    def value(self, x, y):

        Bpol = self.equi.Bpol.value(x,y)
        Babs = self.equi.Babs.value(x,y)

        return Bpol.vector_magnitude/Babs