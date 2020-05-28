# There are a LOT of things that you can choose to plot.
#
# Generally, however, you want to plot a specific group of variables
# 
# UserInterface groups can use the keys of variable_groups to define allowed options for a user
# Feel free to add groups: add a new key, and point it to a list of Variable types

variable_groups = {}

from .BaseVariable import (Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential, NeutralDensity)
from .StaticVariable import (Grid, District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY)
from .StaticVariable import (CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets)
from .EquilibriumVariable import (Psi, Rho, MagneticFieldX, MagneticFieldY, MagneticFieldTor, MagneticField, MagneticFieldAbs, MagneticFieldPol, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch, ParallelUnitVector)
from .DerivedVariable import (SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta, ElectricField, FloatingPotential, SaturationCurrent, ExBVelocity, ParallelElectronVelocity, TotalPressure, ElectronPressure, IonPressure, TotalVelocity)

from source.measurements.Operator import (VectorAbsolute, VectorPoloidalProjection, VectorRadialProjection, VectorParallel)

variable_groups["BaseVariable"] = [Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential]
variable_groups["BaseVariable_w_neutrals"] = variable_groups["BaseVariable"] + [NeutralDensity]

variable_groups["Grid"] = [Grid]
variable_groups["Static"] = [District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY]
variable_groups["Penalisation"] = [CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets]

variable_groups["Alfven"] = [SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta]
variable_groups["Magnetic"] = [Psi, Rho, MagneticFieldPol, MagneticFieldTor, MagneticFieldAbs, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch]
variable_groups["Electric"] = [ScalarPotential, ([VectorAbsolute], ElectricField), ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity)]
variable_groups["Velocity"] = [ParallelIonVelocity, ParallelElectronVelocity, AlfvenSpeed, ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity), SoundSpeed]
variable_groups["Langmuir"] = [Density, ElectronTemperature, FloatingPotential, SaturationCurrent]
variable_groups["Pressure"] = [ElectronPressure, IonPressure, TotalPressure]
variable_groups["PoloidalVelocity"] = [([VectorPoloidalProjection, VectorParallel], ParallelIonVelocity), ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity), ([VectorPoloidalProjection], TotalVelocity)]

variable_groups["TestParallelUnitVector"] = [([VectorRadialProjection], ParallelUnitVector), ([VectorPoloidalProjection], ParallelUnitVector), ([VectorAbsolute], ParallelUnitVector)]
