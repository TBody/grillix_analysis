# For higher order moments, reducing each dimension in turn is not equivalent to 
# all dimensions to a single dimension
# Calling all-reduce keeps a single dimension, and applies a reduction to all other dimensions
# in one step
# If the argument is a vector (i.e. ndims==4) then flatten only the first 3 dimensions

from . import Operator
from source import np
class AllReduction(Operator):
    
    def __init__(self, reduction=np.mean, **kwargs):
        
        super().__init__(**kwargs)
        self.reduction = reduction
        # reduction must have axis and keepdims as possible keyword arguments.
        # Most of the functions at https://docs.scipy.org/doc/numpy/reference/routines.statistics.html are valid
    
    def values(self, z, dimension_to_keep=2):
        
        original_shape = z.shape

        # Reduce all but one dimension to singleton
        new_shape = list(np.ones_like(z.shape))

        # If z is a vector, don't apply over vector dimension
        if z.is_vector:
            assert(original_shape[-1] == 3)
            new_shape[-1] = 3
        
        # Copy the dimension_to_keep shape to the new shape
        new_shape[dimension_to_keep] = original_shape[dimension_to_keep]

        # Prepend a new dimension to the start of the list. Request that its length be enough such that
        # enough to take all of the extra values
        new_shape.insert(0, -1)

        # Reshape the vector to a new_shape
        z_shaped = np.reshape(z, tuple(new_shape))

        # Apply the reduction on the dummy first dimension
        z_reduced = self.reduction(z_shaped, axis=0, keepdims=False)

        return z_reduced