from source.Operator import Operator
from source import np
class TimeReduction(Operator):
    
    def __init__(self, reduction=np.mean, **kwargs):
    
        super().__init__(**kwargs)
        self.reduction = reduction
        # reduction must have axis and keepdims as possible keyword arguments.
        # Most of the functions at https://docs.scipy.org/doc/numpy/reference/routines.statistics.html are valid
    
    def __call__(self, z):
        # Assumes keepdims has been used on each previous operation
        assert(z.ndim==3)
        
        return self.reduction(z, axis=0, keepdims=True)