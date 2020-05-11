from source.Operator import Operator
from source import np
class VectorAbsolute(Operator):
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
    
    def values(self, z):
        
        assert(z.isvector)
        return z.vector_magnitude