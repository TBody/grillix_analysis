from source import np
from .. import Variable

class NeutralDensity(Variable):

    # Any variable defined in terms of variables written into the snaps (or
    # error_snaps) files
    
    def __init__(self):
        super().__init__()
        self.title = "Neutral density"
        
        name_in_netcdf = "neutN"

        # Name of the variable in the snaps netcdfs
        self.name_in_netcdf = name_in_netcdf
        # Array of NetCDFPath (see source.__init__)
        if self.run.directory.use_error_snaps:
            self.snap_netcdf = self.run.directory.neutral_error_snaps
        else:
            self.snap_netcdf = self.run.directory.neutral_snaps
        
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
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.n0
    
    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        
        planes = self.plane_indices[toroidal_slice]
        snaps = self.snap_indices[time_slice]
        points = self.grid_points[poloidal_slice]
        
        values = np.zeros((snaps.size, planes.size, points.size))
        
        for index in planes:
            # Concatenate the perpghost values onto the vgrid
            values[:, index, :] = np.concatenate((
                self.snap_netcdf[index][self.name_in_netcdf][snaps],
                self.snap_netcdf[index][self.name_in_netcdf+"_perpghost"][snaps]
            ), axis=-1)
        
        return values
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        
        return f"{value.to_base_units():6.4g}"