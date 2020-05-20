from . import StaticVariable

class FluxSurface(StaticVariable):
    
    def __init__(self, run=None):
        netcdf_filename = "equi_storage_file"
        title = "Normalised poloidal flux"
        super().__init__('rho', netcdf_filename, title, run=run)
        