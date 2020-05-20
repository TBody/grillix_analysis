from . import PenalisationVariable

class DirectionFunction(PenalisationVariable):
    
    def __init__(self, run=None):
        
        title = "Plate direction"
        netcdf_filename = "penalisation_file"
        super().__init__('pen_xi', netcdf_filename, title, run=run)
        