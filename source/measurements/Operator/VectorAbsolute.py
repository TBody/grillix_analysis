from . import Operator
from source import np
class VectorAbsolute(Operator):
    
    def __init__(self, run=None):
        self.title = "Magnitude"
        
        super().__init__(run=run)
    
    def __call__(self, values, units):
        
        assert(values.is_vector)
        return values.vector_magnitude, units