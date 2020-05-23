from . import Operator
from source import np
from ..WrappedArray import VectorArray

class PadToGrid(Operator):
    
    def __init__(self, constant_val=np.nan, run=None):
        self.constant_val = constant_val
        super().__init__(run=run)
    
    def __call__(self, values, units):
        
        # Pads the last dimension (points) to be the same length as grid
        if values.len_points != self.run.grid.size:

            if values.is_vector:
                pad_width = ((0,0), (0,0), (0, self.run.grid.size-values.shape[-1]), (0, 0))
            else:
                pad_width = ((0,0), (0,0), (0, self.run.grid.size-values.shape[-1]))
            
            # Wrap the np.pad call in __class__, to make sure that values stays a WrappedArray
            values = values.__class__(np.pad(values, pad_width=pad_width, constant_values=self.constant_val, mode='constant'))
        
        return values, units