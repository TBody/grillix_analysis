from . import StaticVariable

class Buffer(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "equi_storage_file"
        self.title = "Buffer"
        self.numerical_variable = False
        super().__init__('buffer_diffusion',  **kwargs)
        
