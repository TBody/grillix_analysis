from . import DerivedVariable
from ..BaseVariable import ElectronTemperature, ScalarPotential
from source import Quantity, unit_registry

class FloatingPotential(DerivedVariable):

    def __init__(self, run=None):
        self.allow_diverging_cmap = False
        self.electron_temperature = ElectronTemperature()
        self.scalar_potential = ScalarPotential()

        self.base_variables = [self.electron_temperature, self.scalar_potential]
        
        title = "Floating Potential"
        
        super().__init__(title, run=None)
    
    @property
    def normalisation_factor(self):
        return self.scalar_potential.normalisation_factor
    
    @property
    def lambda_sh(self):
        return Quantity(self.run.parameters["params_bndconds"]["lambda_sh"], '1/e')

    def fetch_values(self, **kwargs):
        
        scalar_potential = self.dimensional_array(self.scalar_potential(**kwargs))
        electron_temperature = self.dimensional_array(self.electron_temperature(**kwargs))
        
        floating_potential = scalar_potential - self.lambda_sh * electron_temperature

        return self.normalised_ScalarArray(floating_potential)

