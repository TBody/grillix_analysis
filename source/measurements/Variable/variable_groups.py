# There are a LOT of things that you can choose to plot.
#
# Generally, however, you want to plot a specific group of variables (potentially with operators applied)
# 
# UserInterface groups can use the keys of variable_groups to define allowed options for a user
# Feel free to add groups: add a new key, and point it to a list of Variable types
# 
# In addition to "raw" variables, you can also supply tuples which specify a set of operators to apply
# The form of the tuple should be ([LastOperatorToApply, ..., FirstOperatorToApply], Variable)

variable_groups = {}

from .BaseVariable import (Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential, NeutralDensity)
from .StaticVariable import (Grid, District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY)
from .StaticVariable import (CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets)
from .EquilibriumVariable import (Psi, Rho, MagneticFieldX, MagneticFieldY, MagneticFieldTor, MagneticField, MagneticFieldAbs, MagneticFieldPol, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch, ParallelUnitVector)
from .DerivedVariable import (SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta, ElectricField, FloatingPotential, SaturationCurrent, ExBVelocity, ParallelElectronVelocity, TotalPressure, ElectronPressure, IonPressure, TotalVelocity)

from source.measurements.Operator import (VectorAbsolute, VectorPoloidalProjection, VectorRadialProjection, VectorParallel, ParallelGradient)

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

variable_groups["ParallelGradient"] = [([ParallelGradient], Density), ([ParallelGradient], ElectronTemperature), ([ParallelGradient], IonTemperature), ([ParallelGradient], ParallelIonVelocity), ([ParallelGradient], ParallelCurrent), ([ParallelGradient], ScalarPotential), ([ParallelGradient], Vorticity), ([ParallelGradient], ParallelVectorPotential)]

from .DerivedVariable import (IonConvectiveHeatFlux, ElectronConvectiveHeatFlux, IonConductiveHeatFlux, ElectronConductiveHeatFlux)
variable_groups["HeatFlux"] = [([VectorAbsolute], IonConvectiveHeatFlux), ([VectorAbsolute], ElectronConvectiveHeatFlux), ([VectorAbsolute], IonConductiveHeatFlux), ([VectorAbsolute], ElectronConductiveHeatFlux)]
variable_groups["HeatFluxProjections"] = [([VectorPoloidalProjection], IonConvectiveHeatFlux), ([VectorPoloidalProjection], ElectronConvectiveHeatFlux), ([VectorPoloidalProjection], IonConductiveHeatFlux), ([VectorPoloidalProjection], ElectronConductiveHeatFlux), ([VectorRadialProjection], IonConvectiveHeatFlux), ([VectorRadialProjection], ElectronConvectiveHeatFlux), ([VectorRadialProjection], IonConductiveHeatFlux), ([VectorRadialProjection], ElectronConductiveHeatFlux)]