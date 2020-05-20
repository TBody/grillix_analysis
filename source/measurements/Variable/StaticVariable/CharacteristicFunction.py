from . import PenalisationVariable

class CharacteristicFunction(PenalisationVariable):
    
    def __init__(self, run=None):
        
        title = "Characteristic"
        netcdf_filename = "penalisation_file"
        super().__init__('pen_chi', netcdf_filename, title, run=run)
        