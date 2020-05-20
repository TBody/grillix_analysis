from . import Operator
from source import np
class VectorPoloidalProjection(Operator):
    
    def __init__(self, run=None):
        title = "Poloidal"
        super().__init__(run=run)
    
    def values(self, z):

        poloidal_unit_vector = self.run.equilibrium.poloidal_unit_vector()
        assert(z.is_vector)
        assert(poloidal_unit_vector.shape[-2:] == z.shape[-2:])

        return z.dot_product(poloidal_unit_vector)