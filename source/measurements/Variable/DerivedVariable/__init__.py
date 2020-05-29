from .. import Variable

class DerivedVariable(Variable):
    # Variables which are calculated from combinations of BaseVariables and Operators
    # Does not directly access any NetCDF variable

    def __init__(self, title, run=None):
        self.base_variables = getattr(self, "base_variables", [])
        super().__init__(title, run=None)
    
    def set_run(self):
        
        for base_variable in self.base_variables:
            base_variable.run = self.run
    
from .SoundSpeed import SoundSpeed
from .AlfvenSpeed import AlfvenSpeed
from .DynamicalPlasmaBeta import DynamicalPlasmaBeta

from .FloatingPotential import FloatingPotential
from .SaturationCurrent import SaturationCurrent

from .ElectricField import ElectricField
from .ExBVelocity import ExBVelocity
from .ParallelElectronVelocity import ParallelElectronVelocity

from .ElectronPressure import ElectronPressure
from .IonPressure import IonPressure
from .TotalPressure import TotalPressure
from .TotalVelocity import TotalVelocity

from .IonConvectiveHeatFlux import IonConvectiveHeatFlux
from .IonConductiveHeatFlux import IonConductiveHeatFlux
from .IonTotalHeatFlux import IonTotalHeatFlux
from .ElectronConvectiveHeatFlux import ElectronConvectiveHeatFlux
from .ElectronConductiveHeatFlux import ElectronConductiveHeatFlux
from .ElectronTotalHeatFlux import ElectronTotalHeatFlux