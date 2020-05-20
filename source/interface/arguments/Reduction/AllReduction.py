from . import Reduction
from source.measurements.Operator import AllReduction

class AllReductionArg(Reduction):

    def __init__(self, CLI):
        name = "allreduce"
        description = "Function to reduce z to a single dimension"
        super().__init__(CLI, name, description)
    
    def __call__(self):
        return AllReduction(self.HANDLED_FUNCTIONS[self.value])