from . import Variable, ScalarArray
from source import defaultdict, np, Dimensionless

class Grid(Variable):
    
    grid_dict = defaultdict(list, {
        0: "MAIN_GRID",
        1: "PERP_GRID"
    })
    
    def __init__(self, run=None):
        
        super().__init__(title="Grid", run=run)
    
    def set_run(self):
        zeros_main_grid = np.zeros(self.run.grid.main_grid.size)
        ones_perp_grid = np.ones(self.run.grid.perp_grid.size)
        self.grid_values = np.concatenate((zeros_main_grid, ones_perp_grid))

    def fetch_values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return ScalarArray(self.grid_values[poloidal_slice])
    
    def __format_value__(self, value, run=None):
        return self.grid_dict[value]
    
    def values_finalize(self, values, units):
        return values.shape_poloidal(), units