from source import np, Quantity
from .. import Variable

class BaseVariable(Variable):
    # Any variable defined in terms of variables written into the snaps (or
    # error_snaps) files
    
    def __init__(self, name_in_netcdf, title, run=None):
        # Name of the variable in the snaps netcdfs
        self.name_in_netcdf = name_in_netcdf
        self.title = title
        
        super().__init__(run=run)
    
    def set_run(self):
        # Array of NetCDFPath (see source.__init__)
        if self.run.directory.use_error_snaps:
            self.snap_netcdf = self.run.directory.error_snaps
        else:
            self.snap_netcdf = self.run.directory.snaps
        
        # Check if the variable is written to the netcdf as logarithmic or real values
        self.log_in_netcdf = bool(self.snap_netcdf[0][self.name_in_netcdf].logquantity)
        
        # Check how many planes there are, then make an array [0, 1, ..., n_planes - 1] which can be sliced by toroidal_slice
        self.n_planes = len(self.snap_netcdf)
        self.plane_indices = np.arange(self.n_planes)
        
        # Check how many snaps there are, then make an array [0, 1, ..., n_snaps - 1] which can be sliced by time_slice
        self.n_snaps = self.snap_netcdf[0].dimensions['dim_tau'].size
        self.snap_indices = np.arange(self.n_snaps)
        
        # Check how many points there are, then make an array [0, 1, ..., n_full_grid - 1] which can be sliced by poloidal_slice
        self.n_main_grid = self.snap_netcdf[0].dimensions['dim_vgrid'].size
        self.n_perp_grid = self.snap_netcdf[0].dimensions['dim_perpghost'].size
        self.n_full_grid = self.n_main_grid + self.n_perp_grid
        self.grid_points = np.arange(self.n_full_grid)
    
    def fill_values(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        planes = self.plane_indices[toroidal_slice]
        snaps = self.snap_indices[time_slice]
        points = self.grid_points[poloidal_slice]
        
        if type(poloidal_slice) == np.ndarray:
            # Call before testing slice to catch 'np.all/any' request
            if poloidal_slice.dtype == int:
                # Assume index sub-slicing requested
                interior_mask = poloidal_slice[poloidal_slice <= self.n_main_grid]
                exterior_mask = poloidal_slice[poloidal_slice > self.n_main_grid]
            elif poloidal_slice.dtype == bool:
                # Assume mask is given
                interior_mask = poloidal_slice[:self.n_main_grid]
                exterior_mask = poloidal_slice[self.n_main_grid:]
        elif poloidal_slice == slice(None):
            # Assume that interior and exterior mask are the same -- this is dangerous if not loading the whole array
            interior_mask = poloidal_slice
            exterior_mask = poloidal_slice
        else:
            raise NotImplementedError("Unhandled poloidal slice given to BaseVariable")
        
        values = np.zeros((snaps.size, planes.size, points.size))
        
        for index in planes:
            # Concatenate the perpghost values onto the vgrid
            values[:, index, :] = np.concatenate((
                self.snap_netcdf[index][self.name_in_netcdf][snaps, interior_mask],
                self.snap_netcdf[index][self.name_in_netcdf+"_perpghost"][snaps, exterior_mask]
            ), axis=-1)
        if self.log_in_netcdf:
            values = np.exp(values)
        
        return values, self.normalisation_factor

from .Density                 import Density
from .ElectronTemperature     import ElectronTemperature
from .IonTemperature          import IonTemperature
from .ParallelIonVelocity     import ParallelIonVelocity
from .ParallelCurrent         import ParallelCurrent
from .ScalarPotential         import ScalarPotential
from .Vorticity               import Vorticity
from .ParallelVectorPotential import ParallelVectorPotential
from .NeutralDensity          import NeutralDensity