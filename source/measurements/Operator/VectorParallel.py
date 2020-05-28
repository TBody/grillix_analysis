from . import Operator
from source import np
class VectorParallel(Operator):
    # Takes a scalar array and multiplies it by the parallel unit vector
    # This converts quantities like "ParallelIonVelocity" from a magnitude (which
    # is how it is stored/loaded) into a 3D vector

    def __init__(self, run=None):
        super().__init__(run=run)
    
    def __call__(self, values, units):

        parallel_unit_vector, _ = self.run.equilibrium.parallel_unit_vector()
        assert(not(values.is_vector))

        values = parallel_unit_vector * values[..., np.newaxis]

        return values, units