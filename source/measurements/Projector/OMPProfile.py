from source import np, mplcolors
from . import Projector
from source.Variable import FluxSurface

class OMPProfile(Projector):
    
    def __init__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), **kwargs):
        super().__init__(**kwargs)
        self.dimension_to_keep = 2

        self.time_slice = time_slice
        self.toroidal_slice = toroidal_slice
        self.poloidal_slice = slice(None)

    def update_run_values(self):
        self.grid = self.run.grid
        
        rho = FluxSurface(run=self.run)

        rho_values = rho().values.flatten()
        axis_index = np.nanargmin(rho_values)
        self.x_axis = self.grid.x[axis_index]
        self.y_axis = self.grid.y[axis_index]
        
        self.x_axis_index = np.nanargmin(np.abs(self.x_axis-self.grid.x_unique))
        self.y_axis_index = np.nanargmin(np.abs(self.y_axis-self.grid.y_unique))

        self.rho_omp = self.grid.vector_to_matrix(rho_values)[self.y_axis_index, self.x_axis_index:]
    
    def slice_z(self, variable):
        # If setting time_slice, toroidal_slice, or poloidal_slice, must pass as keyword arguments
        
        z_unstructured = variable(self.time_slice, self.toroidal_slice, self.poloidal_slice)
        
        return z_unstructured
    
    def structure_z(self, z_unstructured):
        
        z_reduced = np.squeeze(self.reduction(z_unstructured, dimension_to_keep=self.dimension_to_keep))

        z_structured = self.grid.vector_to_matrix(z_reduced)
        
        return z_structured
    
