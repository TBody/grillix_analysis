from source.Variable.static_base import StaticVariable

class PhiBetweenTargets(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "penalisation_file"
        self.title = "Trace between targets"
        super().__init__('phi_between_targets',  **kwargs)
        