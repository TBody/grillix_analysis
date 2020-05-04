from . import np
from source import unit_registry, Quantity, pint, pd

def setup_vector_to_matrix(self, with_check=False):
    tricolumn_data = np.column_stack((self.x, self.y, np.arange(start=0, stop=len(self.x), dtype=int)))
    pd_dataframe = pd.DataFrame(tricolumn_data, columns=['x', 'y', 'z'])
    # Makes a 2D array of indices
    shaped_data = pd_dataframe.pivot_table(values='z', index='y', columns='x', dropna=False)

    # Flatten array to give a vector
    flattened_data = np.array(shaped_data).flatten()
    # Replaces NaN with zero (will return the z[0] element in this place)
    self.sort_indices = np.nan_to_num(flattened_data).astype('int')
    # Add nan_vector to z[self.sort_indices] to replace z[0] with NaN
    self.nan_vector = np.zeros_like(flattened_data)
    self.nan_vector[np.isnan(flattened_data)] = np.nan

    forward_sort = flattened_data[np.logical_not(np.isnan(self.nan_vector))].astype('int')
    assert(forward_sort.size == self.x.size)

    self.reverse_sort_indices = np.zeros_like(forward_sort)
    self.reverse_sort_indices[forward_sort] = np.arange(forward_sort.size)
    
    self.vector_to_matrix_initialised = True
    if with_check:
        self.check_vector_to_matrix()
        self.check_matrix_to_vector()

def check_vector_to_matrix(self):
    # Generate random vector of values
    unstructured_data = np.random.rand(self.x.size)
    # Make some of the indices nan
    random_indices = np.random.random_integers(low=0, high=unstructured_data.size-1)
    unstructured_data[random_indices] = np.nan

    assert(self.x.shape == unstructured_data.shape)

    # Convert unstructured_data to shaped_data using Pandas method
    tricolumn_data = np.column_stack((self.x, self.y, unstructured_data))
    pd_dataframe = pd.DataFrame(tricolumn_data, columns=['x', 'y', 'z'])
    shaped_data_1 = pd_dataframe.pivot_table(values='z', index='y', columns='x', dropna=False)

    # Convert unstructured_data to shaped_data using vector_to_matrix
    shaped_data_2 = self.vector_to_matrix(unstructured_data)

    assert(np.allclose(shaped_data_1, shaped_data_2, equal_nan=True))

def check_matrix_to_vector(self):
    # Check whether x_mesh and y_mesh can be flattened to match self.x and self.y
    [x_mesh, y_mesh] = np.meshgrid(self.x_unique, self.y_unique)

    assert(np.allclose(self.matrix_to_vector(x_mesh), self.x))
    assert(np.allclose(self.matrix_to_vector(y_mesh), self.y))

def vector_to_matrix_1D(self, unstructured_data):
    assert(self.vector_to_matrix_initialised)
    # If this assertion fails, probably the unstructured_data is for a different grid
    assert(unstructured_data.size == self.x.size), f"Unstructured data shape {unstructured_data.shape} doesn't match grid size {self.x.size}"
    try:
        return (unstructured_data[self.sort_indices] + self.nan_vector).reshape((self.y_unique.size, self.x_unique.size))
    except pint.errors.DimensionalityError:
        nan_vector = Quantity(self.nan_vector, unstructured_data.units)
        return (unstructured_data[self.sort_indices] + nan_vector).reshape((self.y_unique.size, self.x_unique.size))

def vector_to_matrix(self, unstructured_data):
    # Applies vector_to_matrix over the last dimension of an arbitrary dimension array
    return np.apply_along_axis(self.vector_to_matrix_1D, axis=-1, arr=unstructured_data)

def matrix_to_vector(self, structured_data):
    assert(self.vector_to_matrix_initialised)
    # If these assertions fail, the matrix is of the wrong shape (possibly transposed, or defined for a different grid)
    assert(structured_data.shape[1] == self.x_unique.size), f"Dimension 1 of data (shape {structured_data.shape}) did not match x dimension (length {self.x_unique.size})"
    assert(structured_data.shape[0] == self.y_unique.size), f"Dimension 0 of data (shape {structured_data.shape}) did not match y dimension (length {self.y_unique.size})"
    return structured_data.flatten()[np.logical_not(np.isnan(self.nan_vector))][self.reverse_sort_indices]