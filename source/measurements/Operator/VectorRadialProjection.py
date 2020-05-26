from . import Operator
from source import np
class VectorRadialProjection(Operator):

    def __init__(self, run=None):
        self.title = "Radial"
        super().__init__(run=run)

    def __call__(self, values, units):

        radial_unit_vector, _ = self.run.equilibrium.radial_unit_vector()
        assert(values.is_vector)
        assert(radial_unit_vector.shape[-2:] == values.shape[-2:])

        return values.dot_product(radial_unit_vector), units