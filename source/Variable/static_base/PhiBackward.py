from source.Variable.static_base import StaticVariable

class PhiBackward(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "penalisation_file"
        self.title = "Trace against field to plate"
        super().__init__('phi_backward',  **kwargs)
        