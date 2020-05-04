from source import Path, np, Dataset

class Grid:
    
    from ._vector_to_matrix import (setup_vector_to_matrix, 
                                    check_vector_to_matrix,
                                    check_matrix_to_vector,
                                    vector_to_matrix,
                                    vector_to_matrix_1D,
                                    matrix_to_vector
                                    )
    
    from source.shared.properties import (update_run_values, run, convert)
    
    @classmethod
    def from_netcdf(cls, netcdf_file):
        
        grid_file = netcdf_file.open()

        x = grid_file.xmin+(np.array(grid_file.variables['li'])-1)*grid_file.hf
        y = grid_file.ymin+(np.array(grid_file.variables['lj'])-1)*grid_file.hf

        grid_spacing = grid_file.hf

        return cls(x=x, y=y, grid_spacing=grid_spacing)
    
    def __init__(self, x, y, grid_spacing, grid_file=None, test_size=True):
        self.vector_to_matrix_initialised = False
        
        self._x = x
        self._y = y
        
        self._grid_spacing = grid_spacing

        self._x_unique = np.unique(self._x)
        self._y_unique = np.unique(self._y)

        self._xmin = self._x_unique[0]
        self._xmax = self._x_unique[-1]
        self._ymin = self._y_unique[0]
        self._ymax = self._y_unique[-1]
        
        if test_size:
            assert(np.size(self._x) == np.size(self._y))
        self.size = np.size(self._x)

    def update_normalisation_factor(self):
        self.R0 = self.normalisation.R0

    # Auto-convert to normalised when accessing properties, based on self.convert flag
    @property
    def x(self):
        return self._x * self.R0 if self.convert else self._x

    @property
    def y(self):
        return self._y * self.R0 if self.convert else self._y
    
    @property
    def x_unique(self):
        return self._x_unique * self.R0 if self.convert else self._x_unique

    @property
    def y_unique(self):
        return self._y_unique * self.R0 if self.convert else self._y_unique

    @property
    def xmin(self):
        return self._xmin * self.R0 if self.convert else self._xmin

    @property
    def xmax(self):
        return self._xmax * self.R0 if self.convert else self._xmax

    @property
    def ymin(self):
        return self._ymin * self.R0 if self.convert else self._ymin

    @property
    def ymax(self):
        return self._ymax * self.R0 if self.convert else self._ymax
    
    def __add__(self, other):

        new_x = np.append(self._x, other._x)
        new_y = np.append(self._y, other._y)

        return Grid(x=new_x, y=new_y, grid_spacing=self._grid_spacing)
    
    def find_nearest_index(self, x, y, print_error=False):

        # Returns nearest element for linear distance
        nearest_index = np.argmin(np.sqrt((self._x - x)**2 + (self._y - y)**2))

        if print_error:
            print(self._x[nearest_index] - x, self._y[nearest_index] - y)

        if np.size(nearest_index):
            return nearest_index
        else:
            raise RuntimeError("Nearest point is not unique")
    
from .CombinedGrid import CombinedGrid