from . import Reduction
from source.measurements.Operator import ToroidalReduction

class ToroidalReductionArg(Reduction):

    def __init__(self, CLI):
        name = "torreduce"
        description = "Function to reduce z(phi, ...) to z_reduced(...)"
        super().__init__(CLI, name, description)
    
    def __call__(self):
        return ToroidalReduction(self.HANDLED_FUNCTIONS[self.value])