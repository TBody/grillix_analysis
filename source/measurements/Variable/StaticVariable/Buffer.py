from . import StaticVariable

class Buffer(StaticVariable):
    
    def __init__(self, run=None):
        netcdf_filename = "equi_storage_file"
        title = "Buffer"
        self.numerical_variable = False
        super().__init__('buffer_diffusion', netcdf_filename, title, run=run)
        
