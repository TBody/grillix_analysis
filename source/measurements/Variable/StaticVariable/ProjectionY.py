from . import StaticVariable

class ProjectionY(StaticVariable):
    
    def __init__(self, run=None):
        netcdf_filename = "equi_storage_file"
        title = "Polygon projection (y)"
        super().__init__('projection_y', netcdf_filename, title, run=run)
        