from source.Variable import Variable
from source import np

class EquilibriumVariable(Variable):
    # Any variable defined in terms of variables defined by the magnetic equilibria

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def equi(self):
        return self.run.equilibrium
    
    def values_finalize(self, values):
        if self.vector_variable:
            return np.atleast_3d(values).reshape((1,1,-1,3))
        else:
            return np.atleast_3d(values).reshape((1,1,-1))
    
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
