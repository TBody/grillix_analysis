from source.Operator import Operator
from source import np

class PadToGrid(Operator):
    
    def __init__(self, constant_val=np.nan, **kwargs):
        self.constant_val = constant_val
        super().__init__(**kwargs)
    
    def update_run_values(self):
        self.grid = self.run.grid
    
    def __call__(self, z):
        # Assumes keepdims has been used on each previous operation
        assert(z.ndim==3)
        
        # Pads the last dimension (points) to be the same length as grid
        if z.shape[-1] != self.grid.size:
            z = np.pad(z, 
                      ((0,0), (0,0), (0, self.grid.size-z.shape[-1])), constant_values=self.constant_val, mode='constant'
                )
        
        return z