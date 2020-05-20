from . import PenalisationVariable

class PhiForward(PenalisationVariable):
    
    def __init__(self, run=None):
        
        title = "Trace with field to plate"
        netcdf_filename = "penalisation_file"
        super().__init__('phi_forward', netcdf_filename, title, run=run)
        