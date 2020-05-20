from . import BaseVariable

class ParallelCurrent(BaseVariable):
    
    def __init__(self, run=None):
        super().__init__('jparx', 'Current', run=run)
    
    @property
    def normalisation_factor(self):
        return (self.normalisation.c_s0 * self.normalisation.electron_charge * self.normalisation.n0).to(
            'kiloampere*meter**-2')
        