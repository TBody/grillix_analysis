from . import StaticVariable

class ProjectionX(StaticVariable):
    
    def __init__(self, run=None):
        netcdf_filename = "equi_storage_file"
        title = "Polygon projection (x)"
        super().__init__('projection_x', netcdf_filename, title, run=run)
        