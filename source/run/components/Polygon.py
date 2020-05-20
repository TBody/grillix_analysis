from source import plt, np, Dataset
import matplotlib.path as mpltPath

class Polygon:
    
    @classmethod
    def read_polygon_from_trunk(cls, netcdf_file, z_inverted=False):
        
        x_points = np.array(netcdf_file['x'])
        if z_inverted:
            y_points = -np.array(netcdf_file['y'])
        else:
            y_points = np.array(netcdf_file['y'])
        
        if netcdf_file.invert == 1:
            invert_polygon = True
        else:
            invert_polygon = False
        
        return cls(x_points, y_points, invert_polygon)
    
    def __init__(self, x_points, y_points, invert_polygon=False):
        
        self._x_points = np.array(x_points)
        self._y_points = np.array(y_points)
        self.invert_polygon = invert_polygon

        self.polygon = mpltPath.Path(np.column_stack((x_points, y_points)), closed=True)
    
    from source.shared.properties import (update_run_values, update_normalisation_factor, run, convert)

    # Auto-convert to normalised when accessing properties, based on self.convert flag
    @property
    def x_points(self):
        return self._x_points * self.R0 if self.convert else self._x_points

    @property
    def y_points(self):
        return self._y_points * self.R0 if self.convert else self._y_points

    def update_normalisation_factor(self):
        self.R0 =self.normalisation.R0

    def points_inside(self, x_tests, y_tests):

        assert(x_tests.shape == y_tests.shape)
        original_shape = x_tests.shape
        flatten_x = x_tests.reshape((-1))
        flatten_y = y_tests.reshape((-1))
        flatten_z = np.zeros_like(flatten_x)

        for it, x_test, y_test in zip(range(flatten_x.size), flatten_x, flatten_y):
            flatten_z[it] = self.point_inside(x_test, y_test)

        return flatten_z.reshape(original_shape)
    
    def point_inside(self, x_test, y_test):
        # Returns whether a test point (x_test, y_test) is within the polygon
        if not(self.invert_polygon):
            return self.polygon.contains_point([x_test, y_test])
        else:
            return not(self.polygon.contains_point([x_test, y_test]))
    
    def signed_area(self):
        # http://mathworld.wolfram.com/PolygonArea.html
        # Returns the signed area of a non-intersecting polygon
        # If the sign is positive, points are counterclockwise
        # Otherwise, points are clockwise

        n_points = self.x_points.size
        running_sum = 0
        for index in range(n_points):
            running_sum += self.x_points[index] * self.y_points[np.mod(index+1, n_points)] - self.x_points[np.mod(index+1, n_points)] * self.y_points[index]

        return running_sum/2
    
    def plot(self, ax, **kwargs):

        ax.plot(self.x_points, self.y_points, **kwargs)