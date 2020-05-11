from source.Variable.BaseVariable import BaseVariable

class ParallelCurrent(BaseVariable):
    
    def __init__(self, **kwargs):
        super().__init__('jparx', **kwargs)
        self.title = "Current"
        
    def update_normalisation_factor(self):
        self.normalisation_factor = (self.normalisation.c_s0 * self.normalisation.electron_charge * self.normalisation.n0).to(
            'kiloampere*meter**-2'
        )
        