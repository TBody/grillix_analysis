from source import np
from . import PenalisationVariable
from .CharacteristicFunction import CharacteristicFunction

class IntersectionX(PenalisationVariable):
    
    def __init__(self, run=None):
        netcdf_filename = "penalisation_file"
        title = "Polygon intersection (x)"
        super().__init__('intersection_x', netcdf_filename, title, run=run)
    
    def values_finalize(self, values, units):
        [values, units] = super().values_finalize(values, units)
        
        chi, _ = CharacteristicFunction(run=self.run)()

        values[chi == 0] = 0
        values[np.isnan(chi)] = 0

        return values, units