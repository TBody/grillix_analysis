from source.Variable import Variable, Result

class DerivedVariable(Variable):
    # Variables which are calculated from combinations of BaseVariables and Operators
    # Does not directly access any NetCDF variable

    def __init__(self, **kwargs):
        self.derived_variable = True
        self.base_variables = getattr(self, "base_variables", [])
        super().__init__(**kwargs)
    
    def update_run_values(self):
        self.update_base_variables(self.base_variables)
        self.check_base_variables(self.base_variables)
    
    def check_units(self, output):
        if isinstance(output, Result):
            # Downcast to values to prevent wrapping a Result type in itself (not defined)
            output = output.values
        
        if self.convert:
            return output.to(self.normalisation_factor.units)
        elif hasattr(output, "units"):
            return output.to('').magnitude
        else:
            return output

from .SoundSpeed import SoundSpeed
from .AlfvenSpeed import AlfvenSpeed
from .DynamicalPlasmaBeta import DynamicalPlasmaBeta
from .ElectricField import ElectricField
from .FloatingPotential import FloatingPotential
from .SaturationCurrent import SaturationCurrent
from .ExBVelocity import ExBVelocity