from source.Variable.StaticVariable import StaticVariable

class InVessel(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "equi_storage_file"
        self.title = "Point in vessel"
        self.numerical_variable = False
        super().__init__('in_vessel',  **kwargs)
        
