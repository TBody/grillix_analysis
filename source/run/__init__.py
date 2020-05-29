from .Directory import Directory
from .Parameters import Parameters
from .Normalisation import Normalisation
from .Grid import Grid, CombinedGrid
from .Equilibrium import Equilibrium

from source import np
from .components.ContourLevel import find_contour_levels
from .components.Polygon import Polygon
from source.measurements.Variable.StaticVariable import CharacteristicFunction, FluxSurface, PhiForward, PhiBackward

class Run:
    # Data container for constant run attributes

    def __init__(self, filepath, calculate_metainfo=True, use_error_snaps=False):
        # Add a flag whether to convert to SI units or not -- default false since it is easier to calculate in non-normalised units
        self.children = []

        # Resolve the filepaths for the run directory, and read the params.in file
        [self.directory, self.parameters, self.equi_type] = Directory.initialise_and_read_parameters(filepath, use_error_snaps=use_error_snaps)
        self.z_inverted = self.parameters['equi_params']['flip_z']
        
        # Read the physical_parameters.nml file and calculate normalisations
        self.normalisation = Normalisation(self.directory.normalisation_file, with_print=False)

        # Build a combined vgrid + perpghost grid
        self.grid = CombinedGrid(self.directory.main_grid_file, self.directory.perp_grid_file, run=self)
        if self.z_inverted:
            self.grid.invert_z()
        self.grid.setup_vector_to_matrix(with_check=True)
        self.grid.run = self

        try:
            if self.equi_type == "NUMERICAL":
                from .Equilibrium.Numerical import NumericalEquilibrium
                self.equilibrium = NumericalEquilibrium(self.directory.equilibrium_netcdf, run=self)

            elif self.equi_type == "CARTHY":
                from .Equilibrium.Carthy import CarthyEquilibrium
                self.equilibrium = CarthyEquilibrium(run=self)

            elif self.equi_type == "CERFONS":
                from .Equilibrium.Cerfons import CerfonsEquilibrium
                self.equilibrium = CerfonsEquilibrium(run=self)

            elif self.equi_type == "CIRCULAR":
                from .Equilibrium.Circular import CircularEquilibrium
                self.equilibrium = CircularEquilibrium(run=self)

            else:
                raise NotImplementedError(f"No implementation available for {self.equi_type}")
        except Exception as error:
            print(f"Equilibrium read failed with error: {error}. Equilibrium will be unusable.")
        
        if calculate_metainfo:
            
            for function in [
                self.calculate_penalisation_contours,
                self.calculate_parallel_limits,
                self.calculate_divertor_profile,
                self.calculate_exclusion_profile,
                self.calculate_seperatrix,
                self.calculate_in_vessel_mask
                ]:
                try:
                    function()
                except (IndexError, FileNotFoundError, AttributeError):
                    print(f"Unable to calculate run metadata in {function}: missing information")

    @property
    def tau_values(self):
        if self.directory.use_error_snaps:
            snap_netcdf = self.directory.error_snaps
        else:
            snap_netcdf = self.directory.snaps
        
        # Allow plotting without any snaps
        try:
            return np.array(np.atleast_1d(snap_netcdf[0]['tau']))
        except IndexError:
            print("tau values not available")
            return np.atleast_1d([0.0])
    
    @property
    def snap_indices(self):
        return np.arange(np.size(self.tau_values))

    def calculate_penalisation_contours(self):
        
        chi, _ = CharacteristicFunction(run=self)()
    
        max_characteristic = np.nanmax(chi) - np.finfo('float').eps
        levels = np.array([0, 0.5, max_characteristic])
        
        self.penalisation_contours = find_contour_levels(
            self.grid.x_unique, self.grid.y_unique, np.squeeze(self.grid.vector_to_matrix(chi)),
            levels)
        
        for penalisation_contour in self.penalisation_contours:
            penalisation_contour.run = self
    
    def calculate_parallel_limits(self):
        from source.shared.common_functions import smoothstep

        phi_forward, _ = PhiForward(run=self)()
        phi_backward, _ = PhiBackward(run=self)()
        
        # Find the phi-spacing between planes
        chi_width = self.parameters["params_penalisation"]["chi_width"]
        if not(chi_width): chi_width = 5.0
        step_order = self.parameters["params_penalisation"]["step_order"]
        if not(step_order): step_order = 3
        npol = self.parameters["params_grid"]["npol"]

        step_width = chi_width * 2.0 * np.pi / npol

        # Find the point which is 1 parallel spacing away from the chi = 1 line
        # N.b. smoothstep(xc=0, x = phi_forward + step_width/2) would return the chi = 1 line
        #      using xc=-2*np.pi/npol returns a line which is one dphi away from this line
        # step_width and step order have no effect
        backward_trace = np.squeeze(self.grid.vector_to_matrix(smoothstep(2*np.pi/npol, phi_backward-step_width/2, step_width, step_order)))
        forward_trace = np.squeeze(self.grid.vector_to_matrix(smoothstep(-2*np.pi/npol, phi_forward+step_width/2, step_width, step_order)))

        backward_contour = find_contour_levels(self.grid.x_unique, self.grid.y_unique, backward_trace, [0.5])
        forward_contour  = find_contour_levels(self.grid.x_unique, self.grid.y_unique, forward_trace, [0.5])

        self.parallel_limit_contours = [backward_contour[0], forward_contour[0]]
        
        for parallel_limit_contour in self.parallel_limit_contours:
            parallel_limit_contour.run = self
    
    def calculate_divertor_profile(self):
        self.divertor_polygon = Polygon.read_polygon_from_trunk(self.directory.divertor_points_file, self.z_inverted)
        self.divertor_polygon.run = self
    
    def calculate_exclusion_profile(self):
        self.exclusion_polygon = Polygon.read_polygon_from_trunk(self.directory.exclusion_points_file, self.z_inverted)
        self.exclusion_polygon.run = self
    
    def calculate_seperatrix(self):
        flux_surface, _ = FluxSurface(run=self)()
        
        self.seperatrix = find_contour_levels(
            self.grid.x_unique, self.grid.y_unique, np.squeeze(self.grid.vector_to_matrix(flux_surface)),
            [1.0])
        for seperatrix_contour in self.seperatrix:
            seperatrix_contour.run = self
    
    def calculate_in_vessel_mask(self):
        # in_vessel_mask is stored as point indices -- normalisation doesn't matter (should calculate with convert=False: this is the default behaviour)
        
        [x_mesh, y_mesh] = np.meshgrid(self.grid.x_unique, self.grid.y_unique)
        self.in_vessel_mask = self.grid.matrix_to_vector(self.divertor_polygon.points_inside(x_mesh, y_mesh).astype(bool))