from .. import Variable
from source import np

class EquilibriumVariable(Variable):
    # Any variable defined in terms of variables defined by the magnetic equilibria

    def __init__(self, title, run=None):
        super().__init__(title=title, run=run)
    
    @property
    def equi(self):
        return self.run.equilibrium
    
    def values_finalize(self, values, units):
        return values.shape_poloidal(), units
    
from .Psi                import Psi
from .Rho                import Rho
from .MagneticFieldX     import MagneticFieldX
from .MagneticFieldY     import MagneticFieldY
from .MagneticFieldTor   import MagneticFieldTor
from .MagneticField      import MagneticField
from .MagneticFieldAbs   import MagneticFieldAbs
from .MagneticFieldPol   import MagneticFieldPol
from .PoloidalUnitVector import PoloidalUnitVector
from .RadialUnitVector   import RadialUnitVector
from .MagneticFieldPitch import MagneticFieldPitch
