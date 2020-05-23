from . import Grid
from source import np

class CombinedGrid(Grid):
    
    def __init__(self, main_grid_file, perp_grid_file, run):

        self.main_grid = Grid.from_netcdf(main_grid_file, run=run)
        self.perp_grid = Grid.from_netcdf(perp_grid_file, run=run)
        
        full_grid = self.main_grid + self.perp_grid
        
        super().__init__(x=full_grid.x, y=full_grid.y, grid_spacing=full_grid.grid_spacing, run=run)
    
    def invert_z(self):
        # Invert the sub-grids
        self.main_grid.invert_z()
        self.perp_grid.invert_z()
        
        # Invert the combined grid
        self._y = -self._y
        self._y_unique = np.unique(self._y)
        self._ymin = self._y_unique[0]
        self._ymax = self._y_unique[-1]