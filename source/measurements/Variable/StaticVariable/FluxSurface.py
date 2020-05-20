from . import StaticVariable

class FluxSurface(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "equi_storage_file"
        self.title = "Normalised poloidal flux"
        super().__init__('rho',  **kwargs)
        