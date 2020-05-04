from source import Path, np, Dataset

class Grid:
    
    from ._vector_to_matrix import (setup_vector_to_matrix, 
                                    check_vector_to_matrix,
                                    check_matrix_to_vector,
                                    vector_to_matrix,
                                    vector_to_matrix_1D,
                                    matrix_to_vector
                                    )
    
    @classmethod
    def from_netcdf(cls, netcdf_file):

        grid_file = netcdf_file.open()

        x = grid_file.xmin+(np.array(grid_file.variables['li'])-1)*grid_file.hf
        y = grid_file.ymin+(np.array(grid_file.variables['lj'])-1)*grid_file.hf

        grid_spacing = grid_file.hf

        return cls(x=x, y=y, grid_spacing=grid_spacing, grid_file=grid_file)
    
    def __init__(self, x, y, grid_spacing, grid_file=None, test_size=True):
        self.vector_to_matrix_initialised = False
        
        self.x = x
        self.y = y
        
        self.grid_spacing = grid_spacing

        self.x_unique = np.unique(self.x)
        self.y_unique = np.unique(self.y)

        self.xmin = self.x_unique[0]
        self.xmax = self.x_unique[-1]
        self.ymin = self.y_unique[0]
        self.ymax = self.y_unique[-1]
        
        if test_size:
            assert(np.size(self.x) == np.size(self.y))
        self.size = np.size(self.x)
    
    def __add__(self, other):

        new_x = np.append(self.x, other.x)
        new_y = np.append(self.y, other.y)

        return Grid(x=new_x, y=new_y, grid_spacing=self.grid_spacing)
    
    def find_nearest_index(self, x, y, print_error=False):

        # Returns nearest element for linear distance
        nearest_index = np.argmin(np.sqrt((self.x - x)**2 + (self.y - y)**2))

        if print_error:
            print(self.x[nearest_index] - x, self.y[nearest_index] - y)

        if np.size(nearest_index):
            return nearest_index
        else:
            raise RuntimeError("Nearest point is not unique")
    
from .CombinedGrid import CombinedGrid