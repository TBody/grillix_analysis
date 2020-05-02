from source import np
from .Annotate import Annotate

class Projector:

    annotate = Annotate()

    def __init__(self, run=None):
        if run != None:
            self.set_run(run)

    def set_run(self, run):
        self.run = run
        
        if hasattr(self, 'set_values_from_run'):
            self.set_values_from_run()
    
    def __call__(self, variable, **kwargs):
        # If setting time_slice, toroidal_slice, or poloidal_slice, must pass as keyword arguments

        for key, value in kwargs.items():
            if key in self.__dict__.keys():
                if type(value) is not slice:
                    value = np.atleast_1d(value)
                setattr(self, key, value)
            else:
                raise NotImplementedError(f"No attribute {key} found for Projector {self.__class__.__name__}")
        
        return self.slice_and_structure(variable)