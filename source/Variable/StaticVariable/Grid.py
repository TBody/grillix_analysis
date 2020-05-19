from source.Variable.StaticVariable import StaticVariable
from source import defaultdict, np

class Grid(StaticVariable):
    
    grid_dict = defaultdict(list, {
        0: "MAIN_GRID",
        1: "PERP_GRID"
    })
    
    def __init__(self, **kwargs):
        self.netcdf_filename = None
        self.title = "Grid"
        self.numerical_variable = False
        super().__init__('grid',  **kwargs)
    
    def update_run_values(self):
        zeros_main_grid = np.zeros(self.run.grid.main_grid.size)
        ones_perp_grid = np.ones(self.run.grid.perp_grid.size)
        self.grid_values = np.concatenate((zeros_main_grid, ones_perp_grid))

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return self.grid_values[poloidal_slice]
    
    def __format_value__(self, value, **kwargs):
        return self.grid_dict[value]