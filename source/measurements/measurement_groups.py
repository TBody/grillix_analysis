# There are a LOT of things that you can choose to plot.
#
# Generally, however, you want to plot a specific group of variables (potentially with operators applied)
# 
# UserInterface groups can use the keys of measurement_groups to define allowed options for a user
# Feel free to add groups: add a new key, and point it to a list of Variable types
# 
# In addition to "raw" variables, you can also supply tuples which specify a set of operators to apply
# The form of the tuple should be ([LastOperatorToApply, ..., FirstOperatorToApply], Variable)

measurement_groups = {}

from .Operator import (VectorAbsolute, VectorPoloidalProjection, VectorRadialProjection, VectorParallel, ParallelGradient)

# Base variables are written directly into the snap NetCDF
from .Variable.BaseVariable import Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential
measurement_groups["BaseVariable"] = [Density, ElectronTemperature, IonTemperature, ParallelIonVelocity, ParallelCurrent, ScalarPotential, Vorticity, ParallelVectorPotential]

# The neutral density may also be plotted
from .Variable.BaseVariable import NeutralDensity
measurement_groups["BaseVariable_w_neutrals"] = measurement_groups["BaseVariable"] + [NeutralDensity]

# A simple grid plot, showing main grid and perpghost, may be plotted with this variable. Mainly for debugging startup
from .Variable.StaticVariable import Grid
measurement_groups["Grid"] = [Grid]

# Variables written into the metadata file
from .Variable.StaticVariable import District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY
measurement_groups["Static"] = [District, FluxSurface, Buffer, InVessel, ProjectionX, ProjectionY]

# Variables written into the penalisation metadata file
from .Variable.StaticVariable import CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets
measurement_groups["Penalisation"] = [CharacteristicFunction, DirectionFunction, PhiForward, PhiBackward, PhiBetweenTargets]

# Alfven velocity, compared to local sound speed, and local beta
from .Variable.DerivedVariable import SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta
measurement_groups["Alfven"] = [SoundSpeed, AlfvenSpeed, DynamicalPlasmaBeta]

# Magnetic field values
from .Variable.EquilibriumVariable import Psi, Rho, MagneticFieldPol, MagneticFieldTor, MagneticFieldAbs, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch
measurement_groups["Magnetic"] = [Psi, Rho, MagneticFieldPol, ([VectorAbsolute], MagneticFieldPol), MagneticFieldTor, PoloidalUnitVector, RadialUnitVector, MagneticFieldPitch]
# Test that the parallel unit vector and projections are working as expected
from .Variable.EquilibriumVariable import ParallelUnitVector
measurement_groups["TestParallelUnitVector"] = [([VectorRadialProjection], ParallelUnitVector), ([VectorPoloidalProjection], ParallelUnitVector), ([VectorAbsolute], ParallelUnitVector)]

# Electric field and ExB velocity
from .Variable.DerivedVariable import ElectricField, ExBVelocity
measurement_groups["Electric"] = [ScalarPotential, ([VectorAbsolute], ElectricField), ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity)]
# All velocities
from .Variable.DerivedVariable import ParallelElectronVelocity, TotalVelocity
measurement_groups["Velocity"] = [ParallelIonVelocity, ParallelElectronVelocity, AlfvenSpeed, ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity), SoundSpeed]
# Velocities projected into the poloidal plane
measurement_groups["PoloidalVelocity"] = [([VectorPoloidalProjection, VectorParallel], ParallelIonVelocity), ([VectorRadialProjection], ExBVelocity), ([VectorPoloidalProjection], ExBVelocity), ([VectorPoloidalProjection], TotalVelocity)]

# Pressures
from .Variable.DerivedVariable import ElectronPressure, IonPressure, TotalPressure
measurement_groups["Pressure"] = [ElectronPressure, IonPressure, TotalPressure]

# Variables for comparing to Langmuir probe measurements
from .Variable.DerivedVariable import FloatingPotential, SaturationCurrent
measurement_groups["Langmuir"] = [Density, ElectronTemperature, FloatingPotential, SaturationCurrent]

# Parallel gradient of base variables
measurement_groups["ParallelGradient"] = [([ParallelGradient], Density), ([ParallelGradient], ElectronTemperature), ([ParallelGradient], IonTemperature), ([ParallelGradient], ParallelIonVelocity), ([ParallelGradient], ParallelCurrent), ([ParallelGradient], ScalarPotential), ([ParallelGradient], Vorticity), ([ParallelGradient], ParallelVectorPotential)]

# Heat fluxes
from .Variable.DerivedVariable import (IonConvectiveHeatFlux, ElectronConvectiveHeatFlux, IonConductiveHeatFlux, ElectronConductiveHeatFlux, ElectronTotalHeatFlux, IonTotalHeatFlux)
measurement_groups["HeatFlux"] = [([VectorAbsolute], IonConvectiveHeatFlux), ([VectorAbsolute], ElectronConvectiveHeatFlux), ([VectorAbsolute], IonConductiveHeatFlux), ([VectorAbsolute], ElectronConductiveHeatFlux)]
measurement_groups["PoloidalHeatFlux"] = [([VectorPoloidalProjection], IonConvectiveHeatFlux), ([VectorPoloidalProjection], ElectronConvectiveHeatFlux), ([VectorPoloidalProjection], IonConductiveHeatFlux), ([VectorPoloidalProjection], ElectronConductiveHeatFlux), ([VectorRadialProjection], IonConvectiveHeatFlux), ([VectorRadialProjection], ElectronConvectiveHeatFlux), ([VectorRadialProjection], IonConductiveHeatFlux), ([VectorRadialProjection], ElectronConductiveHeatFlux)]
measurement_groups["TotalHeatFlux"] = [([VectorAbsolute], IonTotalHeatFlux), ([VectorPoloidalProjection], IonTotalHeatFlux), ([VectorRadialProjection], IonTotalHeatFlux), ([VectorAbsolute], ElectronTotalHeatFlux), ([VectorPoloidalProjection], ElectronTotalHeatFlux), ([VectorRadialProjection], ElectronTotalHeatFlux)]

from .Variable.StaticVariable import IntersectionX, IntersectionY
measurement_groups["Polygon"] = [IntersectionX, IntersectionY, ProjectionX, ProjectionY]
