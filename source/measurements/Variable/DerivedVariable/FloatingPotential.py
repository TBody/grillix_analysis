from . import DerivedVariable
from ..BaseVariable import ElectronTemperature, ScalarPotential
from source import Quantity, unit_registry

class FloatingPotential(DerivedVariable):
    default_lambda_sh = Quantity(3.1, '1/e')

    def __init__(self, lambda_sh=None, **kwargs):
        if lambda_sh is None:
            self.lambda_sh = self.default_lambda_sh
            print(f"lambda_sh not supplied to FloatingPotential. Using default value {self.lambda_sh}")
        else:
            self.lambda_sh = Quantity(lambda_sh, '1/e')
            print(f"lambda_sh supplied to FloatingPotential. Using lambda_sh = {self.lambda_sh}")

        self.electron_temperature = ElectronTemperature(**kwargs)
        self.scalar_potential = ScalarPotential(**kwargs)

        self.base_variables = [self.electron_temperature, self.scalar_potential]
        
        self.title = "Floating Potential"
        
        super().__init__(**kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.scalar_potential.normalisation_factor
    
    def values(self, **kwargs):
        
        if self.convert:
            output = self.calculate_wrapped(self.scalar_potential(**kwargs).values, self.lambda_sh, self.electron_temperature(**kwargs).values)
        else:
            output = self.scalar_potential(**kwargs) - self.lambda_sh.magnitude * self.electron_temperature(**kwargs)

        return self.check_units(output)
    
    @unit_registry.wraps('V', (None, 'V', '1/e', 'eV'))
    def calculate_wrapped(self, scalar_potential, lambda_sh, electron_temperature):
        return scalar_potential - lambda_sh * electron_temperature
