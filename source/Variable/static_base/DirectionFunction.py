from source.Variable.static_base import StaticVariable

class DirectionFunction(StaticVariable):
    
    def __init__(self, **kwargs):
        self.netcdf_filename = "penalisation_file"
        self.title = "Plate direction"
        super().__init__('pen_xi',  **kwargs)
        