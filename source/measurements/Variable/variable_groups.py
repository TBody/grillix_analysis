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

from .EquilibriumVariable import (Psi, Rho, MagneticFieldX, MagneticFieldY, MagneticFieldTor, MagneticField, MagneticFieldAbs, MagneticFieldPol, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch, ParallelUnitVector)
from .DerivedVariable import (SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta, ElectricField, FloatingPotential, SaturationCurrent, ExBVelocity, ParallelElectronVelocity, TotalPressure, ElectronPressure, IonPressure, TotalVelocity)

from source.measurements.Operator import (VectorAbsolute, VectorPoloidalProjection, VectorRadialProjection, VectorParallel, ParallelGradient)

# Base variables are written directly into the snap NetCDF
from .BaseVariable import Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential
variable_groups["BaseVariable"] = [Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential]

# The neutral density may also be plotted
from .BaseVariable import NeutralDensity
variable_groups["BaseVariable_w_neutrals"] = variable_groups["BaseVariable"] + [NeutralDensity]

# A simple grid plot, showing main grid and perpghost, may be plotted with this variable. Mainly for debugging startup
from .StaticVariable import Grid
variable_groups["Grid"] = [Grid]

# Variables written into the metadata file
from .StaticVariable import District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY
variable_groups["Static"] = [District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY]

# Variables written into the penalisation metadata file
from .StaticVariable import CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets
variable_groups["Penalisation"] = [CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets]

# Alfven velocity, compared to local sound speed, and local beta
from .DerivedVariable import SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta
variable_groups["Alfven"] = [SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta]

# Magnetic field values
from .EquilibriumVariable import Psi, Rho, MagneticFieldPol, MagneticFieldTor, MagneticFieldAbs, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch
variable_groups["Magnetic"] = [Psi, Rho, MagneticFieldPol, MagneticFieldTor, MagneticFieldAbs, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch]
# Test that the parallel unit vector and projections are working as expected
from .EquilibriumVariable import ParallelUnitVector
variable_groups["TestParallelUnitVector"] = [([VectorRadialProjection], ParallelUnitVector), ([VectorPoloidalProjection], ParallelUnitVector), ([VectorAbsolute], ParallelUnitVector)]

# Electric field and ExB velocity
from .DerivedVariable import ElectricField, ExBVelocity
variable_groups["Electric"] = [ScalarPotential, ([VectorAbsolute], ElectricField), ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity)]
# All velocities
from .DerivedVariable import ParallelElectronVelocity
variable_groups["Velocity"] = [ParallelIonVelocity, ParallelElectronVelocity, AlfvenSpeed, ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity), SoundSpeed]
# Velocities projected into the poloidal plane
variable_groups["PoloidalVelocity"] = [([VectorPoloidalProjection, VectorParallel], ParallelIonVelocity), ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity), ([VectorPoloidalProjection], TotalVelocity)]

# Pressures
from .DerivedVariable import ElectronPressure, IonPressure, TotalPressure
variable_groups["Pressure"] = [ElectronPressure, IonPressure, TotalPressure]

# Variables for comparing to Langmuir probe measurements
from .DerivedVariable import FloatingPotential, SaturationCurrent
variable_groups["Langmuir"] = [Density, ElectronTemperature, FloatingPotential, SaturationCurrent]

# Parallel gradient of base variables
variable_groups["ParallelGradient"] = [([ParallelGradient], Density), ([ParallelGradient], ElectronTemperature), ([ParallelGradient], IonTemperature), ([ParallelGradient], ParallelIonVelocity), ([ParallelGradient], ParallelCurrent), ([ParallelGradient], ScalarPotential), ([ParallelGradient], Vorticity), ([ParallelGradient], ParallelVectorPotential)]

# Heat fluxes
from .DerivedVariable import (IonConvectiveHeatFlux, ElectronConvectiveHeatFlux, IonConductiveHeatFlux, ElectronConductiveHeatFlux, ElectronTotalHeatFlux, IonTotalHeatFlux)
variable_groups["HeatFlux"] = [([VectorAbsolute], IonConvectiveHeatFlux), ([VectorAbsolute], ElectronConvectiveHeatFlux), ([VectorAbsolute], IonConductiveHeatFlux), ([VectorAbsolute], ElectronConductiveHeatFlux)]
variable_groups["PoloidalHeatFlux"] = [([VectorPoloidalProjection], IonConvectiveHeatFlux), ([VectorPoloidalProjection], ElectronConvectiveHeatFlux), ([VectorPoloidalProjection], IonConductiveHeatFlux), ([VectorPoloidalProjection], ElectronConductiveHeatFlux), ([VectorRadialProjection], IonConvectiveHeatFlux), ([VectorRadialProjection], ElectronConvectiveHeatFlux), ([VectorRadialProjection], IonConductiveHeatFlux), ([VectorRadialProjection], ElectronConductiveHeatFlux)]
variable_groups["TotalHeatFlux"] = [([VectorAbsolute], IonTotalHeatFlux), ([VectorPoloidalProjection], IonTotalHeatFlux), ([VectorRadialProjection], IonTotalHeatFlux), ([VectorAbsolute], ElectronTotalHeatFlux), ([VectorPoloidalProjection], ElectronTotalHeatFlux), ([VectorRadialProjection], ElectronTotalHeatFlux)]