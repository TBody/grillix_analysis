from . import Equilibrium
from source import np, Quantity
from scipy.interpolate import RectBivariateSpline

class NumericalEquilibrium(Equilibrium):

    def __init__(self, equilibrium_netcdf, run):

        self.netcdf = equilibrium_netcdf
        self.read_magnetic_geometry(run.grid)

        print(f"Using {self.netcdf.description}, {self.netcdf.history}")
        
        super().__init__(run)

    # Define continuous functions
    def psi_func(self, x, y):
        return self.spline_psi(x=x, y=y, grid=False)
    
    def Bx_func(self, x, y):
            #Evaluate the poloidal flux, taking the 0th x derivative and the 1st y derivative
            psi_dZ = self.spline_psi(x=x, y=y, dx=0, dy=1, grid=False)
            
            # N.b. One factor of self%R0 comes from evaluating the derivative on the (x', y') normalised coordinate
            # and the second comes from using normalised x', y' for the axis
            return -psi_dZ / (2 * np.pi * x * self.R0 * self.R0 * self.axis_Btor)
    
    def By_func(self, x, y):
        #Evaluate the poloidal flux, taking the 0th x derivative and the 1st y derivative
        psi_dR = self.spline_psi(x=x, y=y, dx=1, dy=0, grid=False)
        
        # N.b. One factor of self%R0 comes from evaluating the derivative on the (x', y') normalised coordinate
        # and the second comes from using normalised x', y' for the axis
        return psi_dR / (2 * np.pi * x * self.R0 * self.R0 * self.axis_Btor)
    
    def Btor_func(self, x, y):
        return 1/x

    @property
    def psiO(self):
        return self._psiO if self.SI_units else self._psiO.magnitude
    
    @property
    def psiX(self):
        return self._psiX if self.SI_units else self._psiX.magnitude

    # Precompute grid values (same implementation, but uses grid=True to speed up computation)
    def read_magnetic_geometry(self, grid):

        # Keep dimensionless -- useful for returning normalised base values
        self.R0 = self.netcdf['Magnetic_geometry'].magnetic_axis_R
        self.axis_Btor = np.abs(self.netcdf['Magnetic_geometry'].axis_Btor)

        # Convert to Weber
        self._psiO = Quantity(self.netcdf['Psi_limits'].psi_axis, 'Wb')
        self._psiX = Quantity(self.netcdf['Psi_limits'].psi_seperatrix, 'Wb')

        self.spline_R = np.array(self.netcdf['Magnetic_geometry']['R'])
        self.spline_Z = np.array(self.netcdf['Magnetic_geometry']['Z'])
        psi_data = np.array(self.netcdf['Magnetic_geometry']['psi'])

        # Note that the axis ordering is inverted relative to the output of meshgrid.
        self.spline_psi = RectBivariateSpline(self.spline_R, self.spline_Z, psi_data.T)

        # Precompute the grid values of the magnetic fields - store as unstructured arrays (this discards off grid information)
        self.psi_grid_vector = grid.matrix_to_vector(self.spline_psi(x=grid.x_unique, y=grid.y_unique, grid=True).T)

        self.compute_magnetic_field_grid_vectors(grid)

    def compute_magnetic_field_grid_vectors(self, grid):
        self.compute_Bx_grid_vector(grid)
        self.compute_By_grid_vector(grid)
        self.compute_Btor_grid_vector(grid)

    def compute_Bx_grid_vector(self, grid):
        #Evaluate the poloidal flux, taking the 0th x derivative and the 1st y derivative
        psi_dZ = grid.matrix_to_vector(self.spline_psi(x=grid.x_unique, y=grid.y_unique, dx=0, dy=1, grid=True).T)
        
        # N.b. One factor of self%R0 comes from evaluating the derivative on the (x', y') normalised coordinate
        # and the second comes from using normalised x', y' for the axis
        self.Bx_grid_vector = -psi_dZ / (2 * np.pi * grid.x * self.R0 * self.R0 * self.axis_Btor)
    
    def compute_By_grid_vector(self, grid):
        #Evaluate the poloidal flux, taking the 0th x derivative and the 1st y derivative
        psi_dR = grid.matrix_to_vector(self.spline_psi(x=grid.x_unique, y=grid.y_unique, dx=1, dy=0, grid=True).T)
        
        # N.b. One factor of self%R0 comes from evaluating the derivative on the (x', y') normalised coordinate
        # and the second comes from using normalised x', y' for the axis
        self.By_grid_vector = psi_dR / (2 * np.pi * grid.x * self.R0 * self.R0 * self.axis_Btor)
    
    def compute_Btor_grid_vector(self, grid):
        # Assume the magnetic field is given as 1/x

        self.Btor_grid_vector = 1/grid.x
