from . import Reduction
from source.measurements.Operator import TimeReduction

class TimeReductionArg(Reduction):

    def __init__(self, CLI):
        name = "timereduce"
        description = "Function to reduce z(t, ...) to z_reduced(...)"
        super().__init__(CLI, name, description)
    
    def __call__(self):
        return TimeReduction(self.HANDLED_FUNCTIONS[self.value])