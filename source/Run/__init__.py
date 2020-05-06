from .Directory import Directory
from .Parameters import Parameters
from .Normalisation import Normalisation
from .Grid import Grid, CombinedGrid
from .Equilibrium import Equilibrium

from source import np
from source.Variable import CharacteristicFunction, FluxSurface
from source.shared import find_contour_levels, Polygon
from source.Operator import PadToGrid

class Run:
    # Data container for constant run attributes

    def __init__(self, filepath, calculate_metainfo=True):
        # Add a flag whether to convert to SI units or not -- default false since it is easier to calculate in non-normalised units
        self._convert = False
        self.children = []

        # Resolve the filepaths for the run directory, and read the params.in file
        [self.directory, self.parameters, self.equi_type] = Directory.initialise_and_read_parameters(filepath)

        # Read the physical_parameters.nml file and calculate normalisations
        self.normalisation = Normalisation(self.directory.normalisation_file, with_print=False)

        # Build a combined vgrid + perpghost grid
        self.grid = CombinedGrid(self.directory.main_grid_file, self.directory.perp_grid_file)
        self.grid.setup_vector_to_matrix(with_check=True)
        self.grid.run = self

        if self.equi_type == "NUMERICAL":
            from .Equilibrium.Numerical import NumericalEquilibrium
            self.equilibrium = NumericalEquilibrium(self.directory.equilibrium_netcdf, run=self)

        elif self.equi_type == "CARTHY":
            from .Equilibrium.Carthy import CarthyEquilibrium
            self.equilibrium = CarthyEquilibrium(self)

        elif self.equi_type == "CERFONS":
            from .Equilibrium.Cerfons import CerfonsEquilibrium
            self.equilibrium = CerfonsEquilibrium(self)

        elif self.equi_type == "CIRCULAR":
            from .Equilibrium.Circular import CircularEquilibrium
            self.equilibrium = CircularEquilibrium(self)

        else:
            raise NotImplementedError(f"No implementation available for {self.equi_type}")
        
        if calculate_metainfo:
            self.calculate_tau_values()
            self.calculate_penalisation_contours()
            self.calculate_divertor_profile()
            self.calculate_exclusion_profile()
            self.calculate_seperatrix()
            self.calculate_in_vessel_mask()
    
    def add_to_children(self, child_object):
        self.children.append(child_object)

    @property
    def convert(self):
        return self._convert
    
    @convert.setter
    def convert(self, value):
        # Setter for convert
        # N.b. all objects in the analysis routines directly read this value to set their own value for convert
        self._convert = value

    def calculate_tau_values(self):
        if self.directory.use_error_snaps:
            snap_netcdf = self.directory.error_snaps
        else:
            snap_netcdf = self.directory.snaps
        
        self._tau_values = np.array(np.atleast_1d(snap_netcdf[0]['tau']))
    
    @property
    def tau_values(self):
        if self.convert:
            return self._tau_values * self.normalisation.tau_0
        else:
            return self._tau_values

    def calculate_penalisation_contours(self):

        pad_to_grid = PadToGrid(run=self)
        chi = pad_to_grid(CharacteristicFunction(run=self)())
    
        max_characteristic = np.nanmax(chi) - np.finfo('float').eps
        levels = np.array([0, 0.5, max_characteristic])
        
        self.penalisation_contours = find_contour_levels(
            self.grid.x_unique, self.grid.y_unique, np.squeeze(self.grid.vector_to_matrix(chi)),
            levels)
        
        for penalisation_contour in self.penalisation_contours:
            penalisation_contour.run = self
    
    def calculate_divertor_profile(self):
        self.divertor_polygon = Polygon.read_polygon_from_trunk(self.directory.divertor_points_file)
        self.divertor_polygon.run = self
    
    def calculate_exclusion_profile(self):
        self.exclusion_polygon = Polygon.read_polygon_from_trunk(self.directory.exclusion_points_file)
        self.exclusion_polygon.run = self
    
    def calculate_seperatrix(self):
        flux_surface   = FluxSurface(run=self)()
        
        self.seperatrix = find_contour_levels(
            self.grid.x_unique, self.grid.y_unique, np.squeeze(self.grid.vector_to_matrix(flux_surface)),
            [1.0])
        for seperatrix_contour in self.seperatrix:
            seperatrix_contour.run = self
    
    def calculate_in_vessel_mask(self):
        # in_vessel_mask is stored as point indices -- normalisation doesn't matter (should calculate with convert=False: this is the default behaviour)
        
        [x_mesh, y_mesh] = np.meshgrid(self.grid.x_unique, self.grid.y_unique)
        self.in_vessel_mask = self.grid.matrix_to_vector(self.divertor_polygon.points_inside(x_mesh, y_mesh).astype(bool))