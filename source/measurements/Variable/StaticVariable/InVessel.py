from . import StaticVariable

class InVessel(StaticVariable):
    
    def __init__(self, run=None):
        netcdf_filename = "equi_storage_file"
        title = "Point in vessel"
        self.numerical_variable = False
        super().__init__('in_vessel', netcdf_filename, title, run=run)
        
