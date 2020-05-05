from source import Quantity
from .Result import Result, VectorResult

class Variable():
    # Generic variable container
    # Any field which can be plotted should be of this form
    # Data objects must have a Variable object which matches this pattern
    
    def __init__(self, run=None):
        
        # Attributes which can be overwritten by children. If not already set, set defaults
        # Default to dimensionless value
        if not hasattr(self, "normalisation_factor"):
            self.normalisation_factor = Quantity(1, '')
        # display_linear will prevent the variable from converting to logarithmic
        if not hasattr(self, "display_linear"):
            self.display_linear = False
        # numerical_variable means that the variable can be operated on
        if not hasattr(self, "numerical_variable"):
            self.numerical_variable = True
        # vector_variable means that the variable has an additional length (3) dimension, which corresponds to (R, phi, Z) components
        self.vector_variable = getattr(self, "vector_variable", False)

        # Call run at the end, since this triggers a 'set' routine which may depend on the default values
        self.run = run

    from source.shared.properties import (update_run_values, update_normalisation_factor, run, convert)

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return NotImplemented

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        # Read in the values, and apply the appropriate normalisation factor
        
        values = self.values(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)
        
        if self.convert:
            values *= self.normalisation_factor
        
        if self.vector_variable:
            result = VectorResult(values, self, run=self.run, check_shape=True)
        else:
            result = Result(values, self, run=self.run, check_shape=True)
        
        return self.call_finalize(result)
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        if isinstance(value, Quantity):
            return f"{value.to_compact():6.4g}"
        else:
            return f"{value:6.4g}"

    def call_finalize(self, value):
        # Optional function to call before returning values, after the "Result" has been constructed
        return value

from .dynamic_base import (
    Density,
    ElectronTemperature,
    IonTemperature,
    ParallelVelocity,
    ParallelCurrent,
    ScalarPotential,
    Vorticity,
    ParallelVectorPotential,
    NeutralDensity
)
dynamic_base_variables = [Density, ElectronTemperature, IonTemperature, ParallelVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential]

from .static_base import (
    District,
    FluxSurface,
    Buffer,
    InVessel,
    ProjectionX,
    ProjectionY
)
static_base_variables = [District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY]

from .static_base import (
    CharacteristicFunction,
    DirectionFunction,
    PhiForward,
    PhiBackward,
    PhiBetweenTargets
)
penalisation_variables = [CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets]

from .dynamic_derived.SoundSpeed import SoundSpeed
from .dynamic_derived.AlfvenSpeed import AlfvenSpeed
from .dynamic_derived.DynamicalPlasmaBeta import DynamicalPlasmaBeta
from .dynamic_derived.ElectricField import ElectricField
from .dynamic_derived.FloatingPotential import FloatingPotential
from .dynamic_derived.SaturationCurrent import SaturationCurrent

dynamic_derived_variables = [SoundSpeed, SaturationCurrent, FloatingPotential, AlfvenSpeed, DynamicalPlasmaBeta, ElectricField]

electric_field_variables = [ScalarPotential, ElectricField]