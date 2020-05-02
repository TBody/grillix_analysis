from . import Equilibrium
from source import np

class CerfonsEquilibrium(Equilibrium):

    def __init__(self, run):

        self.R0 = None
        self.axis_Btor = None

        self.psiO = None
        self.psiX = None

        self.psi_grid_vector = self.psi_func(x=grid.x, y=grid.y)
        self.compute_magnetic_field_grid_vectors(grid)

        super().__init__(run)
    
    # Define continuous functions
    def psi_func(x, y):
        pass
    
    def Bx_func(x, y):
        pass

    def By_func(x, y):
        pass
    
    def Btor_func(x, y):
        return 1/grid.x

    def compute_magnetic_field_grid_vectors(self, grid):
        self.compute_Bx_grid_vector(grid)
        self.compute_By_grid_vector(grid)
        self.compute_Btor_grid_vector(grid)

    def compute_Bx_grid_vector(self, grid):
        self.Bx_grid_vector = self.Bx_func(x=grid.x, y=grid.y)
    
    def compute_By_grid_vector(self, grid):
        self.By_grid_vector = self.By_func(x=grid.x, y=grid.y)
    
    def compute_Btor_grid_vector(self, grid):
        # Assume the magnetic field is given as 1/x

        self.Btor_grid_vector = 1/grid.x