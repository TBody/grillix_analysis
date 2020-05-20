from source import np
from .. import Variable
from source.measurements.Operator import PadToGrid

class StaticVariable(Variable):
    # Any variable defined in terms of variables written to a metadata file ()
    
    def __init__(self, name_in_netcdf, netcdf_filename, title, run=None):
        
        self.title = title
        self.name_in_netcdf = name_in_netcdf
        self.netcdf_filename = netcdf_filename
        
        super().__init__(run=run)
    
    def set_run(self):
        self.netcdf_file = getattr(self.run.directory, self.netcdf_filename)
    
    def fill_values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.netcdf_file[self.name_in_netcdf]
        
    def values_finalize(self, values):
        if self.vector_variable:
            return np.atleast_3d(values).reshape((1,1,-1,3))
        else:
            return np.atleast_3d(values).reshape((1,1,-1))

class PenalisationVariable(StaticVariable):
    # Variables written to penalisation metadata. Automatically padded to fill full_grid
    
    def set_run(self):
        self.netcdf_file = getattr(self.run.directory, self.netcdf_filename)
        self.pad_to_grid = PadToGrid(run=self.run)
    
    def values_finalize(self, values):
        values = super().values_finalize(values)
        return self.pad_to_grid(values)

# From Grid
from .Grid import Grid

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
