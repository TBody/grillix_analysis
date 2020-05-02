from source.Variable.static_base import StaticVariable

class PhiForward(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "penalisation_file"
        self.title = "Trace with field to plate"
        super().__init__('phi_forward',  **kwargs)
        