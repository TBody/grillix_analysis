from . import Operator
from source import np
class ToroidalReduction(Operator):
    
    def __init__(self, reduction=np.mean, run=None):
        
        super().__init__(run=run)
        self.reduction = reduction
        # reduction must have axis and keepdims as possible keyword arguments.
        # Most of the functions at https://docs.scipy.org/doc/numpy/reference/routines.statistics.html are valid
    
    def values(self, z):
        
        return self.reduction(z, axis=1, keepdims=True)