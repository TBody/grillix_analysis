from source import Path, np, Dataset, Quantity
from source.Variable import Variable
from source.Variable.EquilibriumVariable import (
    Psi,
    Rho,
    MagneticFieldX,
    MagneticFieldY,
    MagneticFieldTor,
    MagneticField,
    MagneticFieldAbs,
    MagneticFieldPol,
    PoloidalUnitVector,
    RadialUnitVector
)

class Equilibrium:

    def __init__(self, run):

        # Give unstructured (x,y) indices so that the Equilibrium variables can be poloidally sliced
        # self.x_array = run.grid.x
        # self.y_array = run.grid.y
        # self.array_size = run.grid.size

        # Before calling super().__init__, the equilibrium subclass should define the following
        # psiO             => O-point poloidal flux (in Weber)
        # psiX             => X-point poloidal flux (in Weber)
        # psi_grid_vector  => psi values in Wb calculated on the grid (unstructured vector form)
        # Bx_grid_vector   => Bx values in T calculated on the grid (unstructured vector form)
        # By_grid_vector   => By values in T calculated on the grid (unstructured vector form)
        # Btor_grid_vector => Btor values in T calculated on the grid (unstructured vector form)
        #
        # Additionally, the equilibrium could define the following
        # psi_func(x,y)   => function which returns psi in Wb for a cartesian point (x,y)
        # Bx_func(x,y)   => function which returns Bx in T for a cartesian point (x,y)
        # By_func(x,y)   => function which returns By in T for a cartesian point (x,y)
        # Btor_func(x,y) => function which returns Btor in T for a cartesian point (x,y)

        self.psi                  = Psi()
        self.rho                  = Rho()
        self.Bx                   = MagneticFieldX()
        self.By                   = MagneticFieldY()
        self.Btor                 = MagneticFieldTor()

        self.Bpol                 = MagneticFieldPol()
        self.Babs                 = MagneticFieldAbs()
        self.poloidal_unit_vector = PoloidalUnitVector()
        self.radial_unit_vector   = RadialUnitVector()

        self.run = run

    from source.shared.properties import (update_normalisation_factor, run, convert)

    def update_run_values(self):
        self.params = self.run.parameters['equi_params']

        for variable in {self.psi, self.rho, self.Bx, self.By, self.Btor,
                         self.Bpol, self.Babs,
                         self.poloidal_unit_vector, self.radial_unit_vector}:
            variable.run = self.run

from .Numerical import NumericalEquilibrium
from .Carthy import CarthyEquilibrium
from .Cerfons import CerfonsEquilibrium
from .Circular import CircularEquilibrium
