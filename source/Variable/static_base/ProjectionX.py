from source.Variable.static_base import StaticVariable

class ProjectionX(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "equi_storage_file"
        self.title = "Polygon projection (x)"
        super().__init__('projection_x',  **kwargs)
        