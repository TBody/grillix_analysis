from source import np, plt
from scipy import interpolate
from ...Component import Component
from source.run.components.ContourLevel import find_contour_levels
from source.run.Equilibrium.Numerical import NumericalEquilibrium
from source.measurements.Variable.StaticVariable import FluxSurface

def interpolate_single(x_query, y_query, x_basis, y_basis, values):
    # Interpolate a single value from a shaped array
    assert(values.ndim == 2)
    assert(values.shape[1] == x_basis.size)
    assert(values.shape[0] == y_basis.size)

    if np.any([
        x_query < x_basis.min(),
        x_query > x_basis.max(),
        y_query < y_basis.min(),
        y_query > y_basis.max()
        ]):
        return np.nan
    
    i0 = np.searchsorted(x_basis, x_query, side='right') - 1
    i1 = min(i0 + 1, x_basis.size - 1)
    j0 = np.searchsorted(y_basis, y_query, side='right') - 1
    j1 = min(j0 + 1, y_basis.size - 1)

    dx0 = x_query - x_basis[i0]
    dy0 = y_query - y_basis[j0]
    dx1 = x_basis[i1] - x_query
    dy1 = y_basis[j1] - y_query

    if i0 == i1:
        wx0 = 1.0
        wx1 = 0.0
    else:
        wx0 = dx1/(dx0+dx1)
        wx1 = dx0/(dx0+dx1)
    
    if j0 == j1:
        wy0 = 1.0
        wy1 = 0.0
    else:
        wy0 = dy1/(dy0+dy1)
        wy1 = dy0/(dy0+dy1)
    
    return (
            wx0*wy0 * values[j0, i0]
        + wx1*wy0 * values[j0, i1]
        + wx0*wy1 * values[j1, i0]
        + wx1*wy1 * values[j1, i1]
    )

def weightings_interpolate(x_query, y_query, x_vector, y_vector):
    # Returns the indices and weightings of neighbours for linear interpolation
    # on the unstructured (x,y,z) tricolumn data
    assert(x_vector.ndim == 1)
    assert(y_vector.ndim == 1)
    assert(x_vector.size == y_vector.size)

    if np.any([
        x_query < x_vector.min(),
        x_query > x_vector.max(),
        y_query < y_vector.min(),
        y_query > y_vector.max()
        ]):
        return [0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]
    
    diff_x = x_query - x_vector
    diff_y = y_query - y_vector

    ix0 = np.nanargmin(np.where(diff_x >= 0, diff_x, np.nan))
    ix1 = np.nanargmax(np.where(diff_x <= 0, diff_x, np.nan))

    iy0 = np.nanargmin(np.where(diff_y >= 0, diff_y, np.nan))
    iy1 = np.nanargmax(np.where(diff_y <= 0, diff_y, np.nan))

    i00 = np.where(np.logical_and(x_vector[ix0] == x_vector, y_vector[iy0] == y_vector))[0][0]
    i01 = np.where(np.logical_and(x_vector[ix0] == x_vector, y_vector[iy1] == y_vector))[0][0]
    i10 = np.where(np.logical_and(x_vector[ix1] == x_vector, y_vector[iy0] == y_vector))[0][0]
    i11 = np.where(np.logical_and(x_vector[ix1] == x_vector, y_vector[iy1] == y_vector))[0][0]
    
    dx0 = x_query - x_vector[ix0]
    dy0 = y_query - y_vector[iy0]
    dx1 = x_vector[ix1] - x_query
    dy1 = y_vector[iy1] - y_query

    if ix0 == ix1:
        wx0 = 1.0
        wx1 = 0.0
    else:
        wx0 = dx1/(dx0+dx1)
        wx1 = dx0/(dx0+dx1)
    
    if iy0 == iy1:
        wy0 = 1.0
        wy1 = 0.0
    else:
        wy0 = dy1/(dy0+dy1)
        wy1 = dy0/(dy0+dy1)
    
    return [i00, i10, i01, i11, wx0*wy0, wx1*wy0, wx0*wy1, wx1*wy1]

def make_matrix_interp(x_vector, y_vector, x_queries, y_queries):
    # Makes a csr matrix which extracts the values at points defined
    # by x_queries, y_queries.
    # csr_matrix * unstructured_data = values at queries
    from scipy.sparse import csr_matrix
    assert(x_vector.ndim == 1)
    assert(y_vector.ndim == 1)
    assert(x_vector.size == y_vector.size)
    assert(x_queries.ndim == 1)
    assert(y_queries.ndim == 1)
    assert(x_queries.size == y_queries.size)

    nz = 0
    indi = []
    indj = []
    val  = []

    for l in range(x_queries.size):
        indi.append(nz)

        [i00, i10, i01, i11, w00, w10, w01, w11] = weightings_interpolate(x_queries[l], y_queries[l], x_vector, y_vector)

        for index, weight in zip([i00, i10, i01, i11], [w00, w10, w01, w11]):
            if weight > 0.0:
                nz += 1
                indj.append(index)
                val.append(weight)
    
    indi.append(nz)

    return csr_matrix((val, indj, indi), shape=(x_queries.size, x_vector.size))

def remove_off_grid_points(run, x_test, y_test):
    flux_surface, _ = FluxSurface(run=run)()
    flux_surface = run.grid.vector_to_matrix(flux_surface.flatten())

    x_test = np.array(x_test)
    y_test = np.array(y_test)
    z_test = np.zeros_like(x_test)

    for x, y, i in zip(x_test, y_test, range(len(x_test))):

        z_test[i] = interpolate_single(x, y, run.grid.x_unique, run.grid.y_unique, flux_surface)

    x_test = x_test[np.logical_not(np.isnan(z_test))]
    y_test = y_test[np.logical_not(np.isnan(z_test))]

    return x_test, y_test

class Interpolator:
    # Base class for interpolators

    def __init__(self, run, key):
        assert(self.x_array.size == self.y_array.size)

        self.key = key
        self.interpolation_matrix = make_matrix_interp(run.grid.x, run.grid.y, self.x_array, self.y_array)
        
        self.calculate_arc_length()
    
    def matrix_vector_multiply_1d(self, unstructured_data):
        return self.interpolation_matrix*unstructured_data

    def __call__(self, unstructured_data):
        assert unstructured_data.shape[-1] == self.interpolation_matrix.shape[-1]
        # Applies interpolation over the last dimension of an arbitrary dimension array
        # Use shift=1 for vector arrays
        is_vector = getattr(unstructured_data, "is_vector", False)
        shift = 1 if is_vector else 0

        return np.apply_along_axis(self.matrix_vector_multiply_1d, axis=(-1-shift), arr=unstructured_data)
    
    def calculate_arc_length(self):

        self.arc_length = np.cumsum(np.insert(np.sqrt(np.diff(self.x_array) ** 2 + np.diff(self.y_array) ** 2), 0, 0.0))
        self.total_arc_length = self.arc_length[-1]
    
    def plot_lineout(self):
        if isinstance(self, PointInterpolator):
            plt.scatter(self.x_array, self.y_array, label=self.key)
        else:
            plt.plot(self.x_array, self.y_array, label=self.key)

class PointInterpolator(Interpolator):

    def __init__(self, run, key, x_point, y_point):

        self.x_array = np.atleast_1d(x_point)
        self.y_array = np.atleast_1d(y_point)

        super().__init__(run, key)

class LineInterpolator(Interpolator):

    def __init__(self, run, key, x_line, y_line, smoothing=1.0, resolution=100):
        
        f, u = interpolate.splprep([x_line, y_line], s=smoothing, per=False)
        x_array, y_array = interpolate.splev(np.linspace(0, 1, resolution), f)
        self.x_array, self.y_array = remove_off_grid_points(run, x_array, y_array)

        super().__init__(run, key)
    
class FluxSurfaceInterpolator(Interpolator):

    def __init__(self, run, key, rho_level=1.0, in_domain=True, closed=False, smoothing=0.0, resolution=100):
        # Mask "False" elements of the mask, since it is easier to apply a district mask
        
        flux_surface, _ = FluxSurface(run=run)()
        flux_surface = np.ma.MaskedArray(run.grid.vector_to_matrix(flux_surface.flatten()), mask=np.logical_not(in_domain))

        contour_level = find_contour_levels(run.grid.x_unique, run.grid.y_unique, flux_surface, [rho_level])

        assert len(contour_level[0].x_arrays) == len(contour_level[0].y_arrays)
        assert len(contour_level[0].x_arrays) > 0, f"No contours found for {key}, rho={rho_level}"
        if not(len(contour_level[0].x_arrays) == 1):
            
            for i in range(len(contour_level[0].x_arrays)):
                plt.plot(contour_level[0].x_arrays[i], contour_level[0].y_arrays[i], label=str(i))
            plt.title(key)
            plt.legend()
            plt.show()
            raise RuntimeError(f"Adjust mask to ensure single continuous contour for {key}, rho={rho_level}")

        x_line = contour_level[0].x_arrays[0]
        y_line = contour_level[0].y_arrays[0]

        f, u = interpolate.splprep([x_line, y_line], s=smoothing, per=closed)
        x_array, y_array = interpolate.splev(np.linspace(0, 1, resolution), f)
        self.x_array, self.y_array = remove_off_grid_points(run, x_array, y_array)

        super().__init__(run, key)
