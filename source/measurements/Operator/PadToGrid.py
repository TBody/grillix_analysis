from . import Operator
from source import np
from ..WrappedArray import VectorArray

class PadToGrid(Operator):
    
    def __init__(self, constant_val=np.nan, run=None):
        self.constant_val = constant_val
        super().__init__(run=run)
    
    def values(self, z):
        
        # Pads the last dimension (points) to be the same length as grid
        if z.shape[2] != self.run.grid.size:

            if isinstance(z, VectorArray):
                pad_width = ((0,0), (0,0), (0, self.run.grid.size-z.shape[-1]), (0, 0))
            else:
                pad_width = ((0,0), (0,0), (0, self.run.grid.size-z.shape[-1]))
            
            z = np.pad(z, pad_width=pad_width, constant_values=self.constant_val, mode='constant')
        
        return z