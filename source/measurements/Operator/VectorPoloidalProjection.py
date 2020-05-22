from . import Operator
from source import np
class VectorPoloidalProjection(Operator):
    
    def __init__(self, run=None):
        self.title = "Poloidal"
        super().__init__(run=run)
    
    def __call__(self, values, units):

        poloidal_unit_vector = self.run.equilibrium.poloidal_unit_vector()
        assert(values.is_vector)
        assert(poloidal_unit_vector.shape[-2:] == values.shape[-2:])

        return values.dot_product(poloidal_unit_vector), units