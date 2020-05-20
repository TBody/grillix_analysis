from . import PenalisationVariable

class PhiBackward(PenalisationVariable):
    
    def __init__(self, run=None):
        
        title = "Trace against field to plate"
        netcdf_filename = "penalisation_file"
        super().__init__('phi_backward', netcdf_filename, title, run=run)
        