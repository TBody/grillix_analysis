from . import Operator
from source import np
class VectorAbsolute(Operator):
    
    def __init__(self, run=None):
        title = "Magnitude"
        
        super().__init__(run=run)
    
    def values(self, z):
        
        assert(z.is_vector)
        return z.vector_magnitude