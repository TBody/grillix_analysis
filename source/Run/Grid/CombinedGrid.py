from . import Grid
# from source import np, defaultdict

# grid_dict = defaultdict(list, {
#     0: "MAIN_GRID",
#     1: "PERP_GRID"
# })

class CombinedGrid(Grid):
    
    def __init__(self, main_grid_file, perp_grid_file, major_radius):
        
        self.main_grid = Grid.from_netcdf(main_grid_file, major_radius)
        self.perp_grid = Grid.from_netcdf(perp_grid_file, major_radius)
        
        full_grid = self.main_grid + self.perp_grid
        
        super().__init__(full_grid.x, full_grid.y, full_grid.grid_spacing, major_radius)
    
    # # Interface allows CombinedGrid to be plotted by PlotPoloidal
    # def compute_values(self):
    #     # Use 0 to indicate main grid
    #     zeros_main_grid = np.zeros(self.main_grid.size)
    #     # Use 1 to indicate perp grid
    #     ones_perp_grid = np.ones(self.perp_grid.size)
        
    #     self.title = 'grid'
    #     self.values = np.concatenate((zeros_main_grid, ones_perp_grid))
    
    # def __format_value__(self, value):
    #     # Formats a z_value
    #     return grid_dict[value]