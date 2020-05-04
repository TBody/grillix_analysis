from source import Quantity

class Variable():
    # Generic variable container
    # Any field which can be plotted should be of this form
    # Data objects must have a Variable object which matches this pattern
    
    def __init__(self, run=None):
        
        if run != None:
            self.set_run(run)
        
        # Attributes which can be overwritten by children
        # Default to dimensionless value, overwrite in child classes
        self.normalisation_factor =  Quantity(1, '')
        # display_linear will prevent the variable from converting to logarithmic
        self.display_linear = False
        # numerical_variable means that the variable can be operated on
        self.numerical_variable = True
    
    def set_run(self, run):
        self.run = run
        self.normalisation = run.normalisation
        if hasattr(self, "set_normalisation_factor"):
            self.set_normalisation_factor()
        
        if hasattr(self, "set_values_from_run"):
            self.set_values_from_run()

    def __call__(self, time_slice=slice(None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        # Generic __call__ signature. Generally overwritten by subclasses, otherwise accesses a
        # attribute z which must be a 3D array z(t,phi,l)
        return self.z[time_slice, toroidal_slice, poloidal_slice]

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
from .static_base import (
    District,
    FluxSurface,
    Buffer,
    InVessel,
    ProjectionX,
    ProjectionY
)
from .static_base import (
    CharacteristicFunction,
    DirectionFunction,
    PhiForward,
    PhiBackward,
    PhiBetweenTargets
)
from .dynamic_derived import (
    SoundSpeed,
    SaturationCurrent,
    FloatingPotential,
    AlfvenSpeed,
    DynamicalPlasmaBeta
)