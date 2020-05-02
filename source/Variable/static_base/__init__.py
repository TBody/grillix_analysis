from source import np
from source.Variable import Variable
from source.shared import QArray

class StaticVariable(Variable):
    # Any variable defined in terms of variables written to a metadata file ()
    
    def __init__(self, name_in_netcdf, **kwargs):
        
        # Name of the variable in the snaps netcdfs
        self.name_in_netcdf = name_in_netcdf
        # Array of NetCDFPath (see source.__init__)
        
        super().__init__(**kwargs)
    
    def set_values_from_run(self):
        self.netcdf_file = getattr(self.run.directory, self.netcdf_filename)
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = self.netcdf_file[self.name_in_netcdf]
        
        return QArray.init_poloidal(values, self.normalisation_factor)

# From equilibrium storage
from .District               import District
from .FluxSurface            import FluxSurface
from .Buffer                 import Buffer
from .InVessel               import InVessel
from .ProjectionX            import ProjectionX
from .ProjectionY            import ProjectionY

# From penalisation metadata
from .CharacteristicFunction import CharacteristicFunction
from .DirectionFunction      import DirectionFunction
from .PhiForward             import PhiForward
from .PhiBackward            import PhiBackward
from .PhiBetweenTargets      import PhiBetweenTargets
