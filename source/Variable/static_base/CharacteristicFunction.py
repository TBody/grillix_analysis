from source.Variable.static_base import StaticVariable

class CharacteristicFunction(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "penalisation_file"
        self.title = "Characteristic"
        super().__init__('pen_chi', **kwargs)
        