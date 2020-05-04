from source import Quantity

class Variable():
    # Generic variable container
    # Any field which can be plotted should be of this form
    # Data objects must have a Variable object which matches this pattern
    
    def __init__(self, run=None):
        self.run = run
        
        # Attributes which can be overwritten by children
        # Default to dimensionless value, overwrite in child classes
        self.normalisation_factor = Quantity(1, '')
        # display_linear will prevent the variable from converting to logarithmic
        self.display_linear = False
        # numerical_variable means that the variable can be operated on
        self.numerical_variable = True
    
    from source.shared.properties import (update_run_values, update_normalisation_factor, run, convert)

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        # Read in the values, and apply the appropriate normalisation factor
        
        values = self.values(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)
        
        if self.convert:
            values *= self.normalisation_factor
        
        return values
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        if isinstance(value, Quantity):
            return f"{value.to_compact():6.4g}"
        else:
            return f"{value:6.4g}"

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

from .dynamic_derived import (
    SoundSpeed,
    SaturationCurrent,
    FloatingPotential,
    AlfvenSpeed,
    DynamicalPlasmaBeta
)
dynamic_derived_variables = [SoundSpeed, SaturationCurrent, FloatingPotential, AlfvenSpeed, DynamicalPlasmaBeta]