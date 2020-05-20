from . import PenalisationVariable

class PhiBetweenTargets(PenalisationVariable):
    
    def __init__(self, run=None):
        
        title = "Trace between targets"
        netcdf_filename = "penalisation_file"
        super().__init__('phi_between_targets', netcdf_filename, title, run=run)
        