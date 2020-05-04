from source.Variable.dynamic_derived import DerivedDynamicVariable
from source.Variable.dynamic_base import ElectronTemperature, ScalarPotential

class FloatingPotential(DerivedDynamicVariable):
    default_lambda_sh = 3.1

    def __init__(self, lambda_sh=None, **kwargs):
        if lambda_sh is None:
            self.lambda_sh = self.default_lambda_sh
            print(f"lambda_sh not supplied to FloatingPotential. Using default value {self.lambda_sh}")
        else:
            self.lambda_sh = lambda_sh
            print(f"lambda_sh supplied to FloatingPotential. Using lambda_sh = {self.lambda_sh}")

        self.electron_temperature = ElectronTemperature(**kwargs)
        self.scalar_potential = ScalarPotential(**kwargs)
        
        self.title = "Floating Potential"
        
        super().__init__(**kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.scalar_potential.normalisation_factor
    
    def update_run_values(self):
        self.check_base_variables([self.electron_temperature, self.scalar_potential])
        
    def values(self, **kwargs):

        return self.scalar_potential.values(**kwargs) - self.lambda_sh * self.electron_temperature.values(**kwargs)
