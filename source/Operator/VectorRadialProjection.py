from source.Operator import Operator
from source import np
class VectorRadialProjection(Operator):
    
    def __init__(self, reduction=np.mean, **kwargs):
        
        super().__init__(**kwargs)
    
    def values(self, z):
        
        assert(z.isvector)
        return NotImplemented