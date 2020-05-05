from source.Operator import Operator
from source import np
class TimeReduction(Operator):
    
    def __init__(self, reduction=np.mean, **kwargs):
    
        super().__init__(**kwargs)
        self.reduction = reduction
        # reduction must have axis and keepdims as possible keyword arguments.
        # Most of the functions at https://docs.scipy.org/doc/numpy/reference/routines.statistics.html are valid
    
    def values(self, z):
        
        return self.reduction(z, axis=0, keepdims=True)