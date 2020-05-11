from source.Operator import Operator
from source import np
class VectorAbsolute(Operator):
    
    def __init__(self, **kwargs):
        self.title = "Magnitude"
        
        super().__init__(**kwargs)
    
    def values(self, z):
        
        assert(z.is_vector)
        return z.vector_magnitude