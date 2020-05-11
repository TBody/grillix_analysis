from source.Operator import Operator
from source import np
class VectorRadialProjection(Operator):

    def __init__(self, **kwargs):
        self.title = "Radial"
        super().__init__(**kwargs)

    def values(self, z):

        radial_unit_vector = self.run.equilibrium.radial_unit_vector()
        assert(z.is_vector)
        assert(radial_unit_vector.shape[-2:] == z.shape[-2:])

        return z.dot_product(radial_unit_vector)