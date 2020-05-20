from . import StaticVariable
from source import defaultdict, np

class Grid(StaticVariable):
    
    grid_dict = defaultdict(list, {
        0: "MAIN_GRID",
        1: "PERP_GRID"
    })
    
    def __init__(self, run=None):
        netcdf_filename = None
        title = "Grid"
        self.numerical_variable = False
        super().__init__('grid', netcdf_filename, title, run=run)
    
    def set_run(self):
        zeros_main_grid = np.zeros(self.run.grid.main_grid.size)
        ones_perp_grid = np.ones(self.run.grid.perp_grid.size)
        self.grid_values = np.concatenate((zeros_main_grid, ones_perp_grid))

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.grid_values[poloidal_slice]
    
    def __format_value__(self, value, run=None):
        return self.grid_dict[value]