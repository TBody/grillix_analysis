from source import np
from source.Variable import Variable
from source.Operator import PadToGrid

class StaticVariable(Variable):
    # Any variable defined in terms of variables written to a metadata file ()
    
    def __init__(self, name_in_netcdf, **kwargs):
        
        # Name of the variable in the snaps netcdfs
        self.name_in_netcdf = name_in_netcdf
        # Array of NetCDFPath (see source.__init__)
        
        super().__init__(**kwargs)
    
    def update_run_values(self):
        self.netcdf_file = getattr(self.run.directory, self.netcdf_filename)
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = self.netcdf_file[self.name_in_netcdf]
        
        return np.atleast_3d(values).reshape((1,1,-1))

class PenalisationVariable(StaticVariable):
    # Variables written to penalisation metadata. Automatically padded to fill full_grid
    def __init__(self, name_in_netcdf, **kwargs):
        self.netcdf_filename = "penalisation_file"
        super().__init__(name_in_netcdf, **kwargs)
    
    def update_run_values(self):
        self.netcdf_file = getattr(self.run.directory, self.netcdf_filename)
        self.pad_to_grid = PadToGrid(run=self.run)
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = self.netcdf_file[self.name_in_netcdf]
        
        return self.pad_to_grid(np.atleast_3d(values).reshape((1,1,-1)))

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
