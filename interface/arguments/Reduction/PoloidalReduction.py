from . import Reduction
from source.Operator import PoloidalReduction

class PoloidalReductionArg(Reduction):

    def __init__(self, CLI):
        name = "polreduce"
        description = "Function to reduce z(l, ...) to z_reduced(...)"
        super().__init__(CLI, name, description)
    
    def __call__(self):
        return PoloidalReduction(self.HANDLED_FUNCTIONS[self.value])