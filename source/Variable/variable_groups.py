# There are a LOT of things that you can choose to plot.
#
# Generally, however, you want to plot a specific group of variables
# The easiest way to do this is to call
# 
#   figure.set_data_array(run=run, projector=projector, variables=variable_groups[key], operators=operators)
# 
# UserInterface groups can use the keys of variable_groups to define allowed options for a user
# Feel free to add groups: add a new key, and point it to a list of Variable types

variable_groups = {}

from .BaseVariable import (Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential, NeutralDensity)
from .StaticVariable import (District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY)
from .StaticVariable import (CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets)
from .EquilibriumVariable import (Psi, Rho, MagneticFieldX, MagneticFieldY, MagneticFieldTor, MagneticField, MagneticFieldAbs, MagneticFieldPol, PoloidalUnitVector, RadialUnitVector)
from .DerivedVariable import (SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta, ElectricField, FloatingPotential, SaturationCurrent)

from source.Operator import (VectorAbsolute, VectorPoloidalProjection, VectorRadialProjection)

variable_groups["BaseVariable"] = [Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential]
variable_groups["BaseVariable_w_neutrals"] = variable_groups["BaseVariable"] + [NeutralDensity]
variable_groups["StaticVariable"] = [District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY]
variable_groups["penalisation"] = [CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets]
variable_groups["dynamic_derived"] = [SoundSpeed, SaturationCurrent, FloatingPotential, AlfvenSpeed, DynamicalPlasmaBeta, ElectricField]
variable_groups["magnetic_field"] = [Psi, Rho, MagneticFieldPol, MagneticFieldTor, MagneticFieldAbs, PoloidalUnitVector, RadialUnitVector]
variable_groups["electric_field"] = [ScalarPotential, ElectricField, ([VectorAbsolute], ElectricField)]
