from source.Variable.StaticVariable import StaticVariable

class ProjectionY(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "equi_storage_file"
        self.title = "Polygon projection (y)"
        super().__init__('projection_y',  **kwargs)
        