from source import Path, np, Dataset, Quantity
from source.Variable import Variable
from source.shared import Vector, VectorQArray, QArray

class Equilibrium:

    def __init__(self, run):

        self.normalisation = run.normalisation
        self.params = run.parameters['equi_params']

        # Give unstructured (x,y) indices so that the Equilibrium variables can be poloidally sliced
        self.x_array = run.grid.x
        self.y_array = run.grid.y
        self.array_size = run.grid.size

        # Before calling super().__init__, the equilibrium subclass should define the following
        # psiO             => O-point poloidal flux (in Weber) 
        # psiX             => X-point poloidal flux (in Weber)
        # psi_grid_vector  => psi values calculated on the grid (unstructured vector form)
        # Bx_grid_vector   => Bx values calculated on the grid (unstructured vector form)
        # By_grid_vector   => By values calculated on the grid (unstructured vector form)
        # Btor_grid_vector => Btor values calculated on the grid (unstructured vector form)
        # 
        # Additionally, the equilibrium could define the following
        # psi_func(x,y)   => function which returns psi for a cartesian point (x,y)
        # Bx_func(x,y)   => function which returns Bx for a cartesian point (x,y)
        # By_func(x,y)   => function which returns By for a cartesian point (x,y)
        # Btor_func(x,y) => function which returns Btor for a cartesian point (x,y)

        self.psi                  = Psi(self, run=run)
        self.rho                  = Rho(self, run=run)
        self.Bx                   = MagneticFieldX(self, run=run)
        self.By                   = MagneticFieldY(self, run=run)
        self.Btor                 = MagneticFieldTor(self, run=run)

        self.Bpol                 = MagneticFieldPol(self, run=run)
        self.Babs                 = MagneticFieldAbs(self, run=run)
        self.poloidal_unit_vector = PoloidalUnitVector(self, run=run)
        self.radial_unit_vector   = RadialUnitVector(self, run=run)

from .Numerical import NumericalEquilibrium
from .Carthy import CarthyEquilibrium
from .Cerfons import CerfonsEquilibrium
from .Circular import CircularEquilibrium

class EquilibriumVariable(Variable):
    # Any variable defined in terms of variables defined by the magnetic equilibria

    def __init__(self, equi, **kwargs):
        self.equi = equi
        super().__init__(**kwargs)

    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        raise NotImplementedError("No __call__ implementation found for variable")

class Psi(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "Poloidal Flux"

    def set_normalisation_factor(self):
        self.normalisation_factor = Quantity(1, 'weber')
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return QArray(self.equi.psi_grid_vector[poloidal_slice], self.normalisation_factor)
    
    def value(self, x, y):
        return self.equi.psi_func(x, y)

class Rho(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "Norm. poloidal Flux"

    def set_normalisation_factor(self):
        self.normalisation_factor = Quantity(1, '')
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        psi = self.equi.psi(poloidal_slice)
        
        # Make values which would give rho < 0 return rho = 0
        psi[np.where(psi > self.equi.psiO)] = self.equi.psiO
        
        return QArray(np.sqrt((psi - self.equi.psiO)/(self.equi.psiX - self.equi.psiO)), self.normalisation_factor)
    
    def value(self, x, y):
        return self.equi.psi_func.value(x,y)

class MagneticFieldX(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "B x"

    def set_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return QArray(self.equi.Bx_grid_vector[poloidal_slice], self.normalisation_factor)
    
    def value(self, x, y):
        return self.equi.Bx_func.value(x,y)

class MagneticFieldY(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "B y"

    def set_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return QArray(self.equi.By_grid_vector[poloidal_slice], self.normalisation_factor)
    
    def value(self, x, y):
        return self.equi.By_func.value(x,y)

class MagneticFieldTor(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "B toroidal"

    def set_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return QArray(self.equi.Btor_grid_vector[poloidal_slice], self.normalisation_factor)
    
    def value(self, x, y):
        return self.equi.Btor_func.value(x,y)

class MagneticFieldPol(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "B poloidal"

    def set_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = np.sqrt(self.equi.Bx_grid_vector[poloidal_slice]**2 + self.equi.By_grid_vector[poloidal_slice]**2)
        return QArray(values, self.normalisation_factor)
    
    def value(self, x, y):
        return np.sqrt(self.equi.Bx_func(x,y)**2 + self.equi.By_func(x,y)**2)

class MagneticFieldAbs(EquilibriumVariable):

    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)
        self.title = "magnitude(B)"

    def set_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.B0
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = np.sqrt(self.equi.Bx_grid_vector[poloidal_slice]**2 + self.equi.By_grid_vector[poloidal_slice]**2 + self.equi.Btor_grid_vector[poloidal_slice]**2)
        return QArray(values, self.normalisation_factor)
    
    def value(self, x, y):
        return np.sqrt(self.equi.Bx_func(x,y)**2 + self.equi.By_func(x,y)**2 + self.equi.Btor_func(x,y)**2)

class District(EquilibriumVariable):
    # N.b. this is already written out as a static variable in equi_storage.nc
    # Don't have to double-implement, but can if you want to check
    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)

        self.title = "District"
        self.numerical_variable = False

class PoloidalUnitVector(EquilibriumVariable):
    # Unit vector along the flux surface
    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)

        self.title = "Poloidal unit vector"
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        Bx = self.equi.Bx_grid_vector[poloidal_slice]
        By = self.equi.By_grid_vector[poloidal_slice]
        Bpol = np.sqrt(Bx**2 + By**2)

        values = VectorQArray(R = Bx/Bpol, Z = By/Bpol, phi = 0, normalisation_factor=self.normalisation_factor)
        return values
    
    def value(self, x, y):
        Bx = self.equi.Bx_func(x,y)
        By = self.equi.By_func(x,y)
        Bpol = np.sqrt(Bx**2 + By**2)

        return Vector(R = Bx/Bpol, Z = By/Bpol, phi = 0)

class RadialUnitVector(EquilibriumVariable):
    # Unit vector across the flux surface
    def __init__(self, equi, **kwargs):
        super().__init__(equi, **kwargs)

        self.title = "Radial unit vector"

    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):

        Bx = self.equi.Bx_grid_vector[poloidal_slice]
        By = self.equi.By_grid_vector[poloidal_slice]
        Bpol = np.sqrt(Bx**2 + By**2)

        values = VectorQArray(R = -By/Bpol, Z = Bx/Bpol, phi = 0, normalisation_factor=self.normalisation_factor)
        return values
    
    def value(self, x, y):
        Bx = self.equi.Bx_func(x,y)
        By = self.equi.By_func(x,y)
        Bpol = np.sqrt(Bx**2 + By**2)

        return Vector(R = -By/Bpol, Z = Bx/Bpol, phi = 0)
