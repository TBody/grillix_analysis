from source import np, Quantity
from . import Operator
from ..WrappedArray import WrappedArray

def reduction_mean(values, axis, keepdims=True):
    return np.mean(values, axis=axis, keepdims=keepdims)

def reduction_median(values, axis, keepdims=True):
    return np.median(values, axis=axis, keepdims=keepdims)

def reduction_std(values, axis, keepdims=True):
    return np.std(values, axis=axis, keepdims=keepdims)

reduction_functions = {
    "mean": reduction_mean,
    "median": reduction_median,
    "std": reduction_std
}

class Reduction(Operator):

    def __init__(self, reduction, run=None):
        super().__init__(run=run)
        self.reduction = reduction

    def reduce_extra_dimensions(self, values, units, keep_time=False):
        if keep_time:
            assert(isinstance(self, ReduceTo1D)), f"keep_time open should only be used with ReduceTo1D"
        
        # Check dimensions before, to make sure that the correct shape has been passed
        values.check_dimensions()
        [values, units] = self.__call__(values, units, keep_time)
        # Reductions should keep the same number of dimensions
        values.check_dimensions()
        # Squeeze out all length-1 dimensions
        values = np.squeeze(values)

        # Check that the returned objects are of the correct types
        assert(isinstance(values, WrappedArray))
        assert(isinstance(units, Quantity))
        
        # Check that the squeezing has had the desired effect
        
        if values.is_vector:
            assert(values.ndim == 2 if not keep_time else 3)
            assert(values.shape[-1] == 3)
        else:
            assert(values.ndim == 1 if not keep_time else 2)
        
        return values, units

class PoloidalReduction(Reduction):

    def __call__(self, values, units, keep_time=False):
        return self.reduction(values, axis=values.dim_points), units

class TimeReduction(Reduction):

    def __call__(self, values, units, keep_time=False):
        return self.reduction(values, axis=values.dim_time), units

class ToroidalReduction(Reduction):

    def __call__(self, values, units, keep_time=False):
        return self.reduction(values, axis=values.dim_phi), units

class ReduceTo1D(Reduction):
    # For higher order moments, reducing each dimension in turn is not equivalent to 
    # all dimensions to a single dimension
    # Calling all-reduce keeps a single dimension, and applies a reduction to all other dimensions
    # in one step
    # If the argument is a vector (i.e. ndims==4) then flatten only the first 3 dimensions

    def reduce_all_except(self, values, dimension_to_keep, keep_time=False):
        
        original_shape = values.shape

        # Reduce all but one dimension to singleton
        new_shape = list(np.ones_like(values.shape))

        # If values is a vector, don't apply over vector dimension
        if values.is_vector:
            assert(original_shape[-1] == 3)
            new_shape[-1] = 3
        
        # Copy the dimension_to_keep shape to the new shape
        new_shape[dimension_to_keep] = original_shape[dimension_to_keep]
        # If keep_time, also keep the time dimension
        if keep_time:
            new_shape[values.dim_time] = original_shape[values.dim_time]

        # Prepend a new dimension to the start of the list. Request that its length be enough such that
        # enough to take all of the extra values
        new_shape.insert(0, -1)

        # Reshape the vector to a new_shape
        z_shaped = np.reshape(values, tuple(new_shape))

        # Apply the reduction on the dummy first dimension (keepdims=False to eliminate the new dimension)
        z_reduced = self.reduction(z_shaped, axis=0, keepdims=False)

        return z_reduced
    
    def cast_to_subclass(self, cls):
        # Can initialise a generic ReduceTo1D object, with a defined reduction, and
        # then convert it to a subclass to determine which dimension should be operated on
        assert(type(cls) == type)
        
        if self.run != None:
            new_object = cls(reduction=self.reduction, run=self.run)
        else:
            new_object = cls(reduction=self.reduction)
        
        assert(isinstance(new_object, ReduceTo1D))
        return new_object

class ReduceToPoloidal(ReduceTo1D):

    def __call__(self, values, units, keep_time=False):
        return self.reduce_all_except(values, dimension_to_keep=values.dim_points, keep_time=keep_time), units

class ReduceToTime(ReduceTo1D):

    def __call__(self, values, units, keep_time=False):
        # Already keeping time
        return self.reduce_all_except(values, dimension_to_keep=values.dim_time), units

class ReduceToToroidal(ReduceTo1D):

    def __call__(self, values, units, keep_time=False):
        return self.reduce_all_except(values, dimension_to_keep=values.dim_phi, keep_time=keep_time), units