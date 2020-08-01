from source import np, plt
from . import Projector
from ..Operator import ReduceToPoloidal
from scipy import interpolate
from source.run.Equilibrium.Numerical import NumericalEquilibrium
from source.measurements.Variable.StaticVariable import FluxSurface

class Lineout(Projector):
    
    def __init__(self, lineout_key, run=None, resolution=100):
        self.resolution = resolution
        self.lineout_key = lineout_key
        super().__init__(run=run)

    def request_reduction(self, reduction):
        return reduction.cast_to_subclass(ReduceToPoloidal)

    def set_run(self):
        self.grid = self.run.grid
        self.set_arrays(self.run)

    def set_arrays(self, run):
        assert(isinstance(run.equilibrium, NumericalEquilibrium)), f"Only implemented for Numerical equilibrium"
        equi = run.equilibrium
    
        if self.lineout_key == "OMP":
            self.x_lineout = np.linspace(1.0, run.grid.xmax)
            self.y_lineout = np.ones_like(self.x_lineout)*(equi.Z0 / equi.R0)
        
        elif self.lineout_key == "IMP":
            self.x_lineout = np.linspace(run.grid.xmin, 1.0)
            self.y_lineout = np.ones_like(self.x_lineout)*(equi.Z0 / equi.R0)        
        
        elif self.lineout_key == "MP":
            self.x_lineout = np.linspace(run.grid.xmin, run.grid.xmax)
            self.y_lineout = np.ones_like(self.x_lineout)*(equi.Z0 / equi.R0)

        elif self.lineout_key == "VMP":
            self.y_lineout = np.linspace(equi.Z0/equi.R0, run.grid.ymax)
            self.x_lineout = np.ones_like(self.y_lineout)
        
        elif self.lineout_key == "LFS_C0":
            self.x_lineout = run.penalisation_contours[0].x_arrays[1]
            self.y_lineout = run.penalisation_contours[0].y_arrays[1]

        elif self.lineout_key == "LFS_TARGET":
            self.x_lineout = run.penalisation_contours[1].x_arrays[1]
            self.y_lineout = run.penalisation_contours[1].y_arrays[1]

        elif self.lineout_key == "HFS_C0":
            self.x_lineout = run.penalisation_contours[0].x_arrays[0]
            self.y_lineout = run.penalisation_contours[0].y_arrays[0]

        elif self.lineout_key == "HFS_TARGET":
            self.x_lineout = run.penalisation_contours[1].x_arrays[0]
            self.y_lineout = run.penalisation_contours[1].y_arrays[0]
        
        elif self.lineout_key == "AX":
            self.x_lineout = np.linspace(run.grid.xmin, run.grid.xmax, 100)
            self.y_lineout = equi.point_axis(x=self.x_lineout, R_centre=equi.RX/equi.R0, Z_centre=equi.ZX/equi.R0)
        
        elif self.lineout_key == "AXPX":
            self.x_lineout = np.linspace(run.grid.xmin, run.grid.xmax, 100)
            self.y_lineout = equi.point_axis(x=self.x_lineout, R_centre=equi.RX/equi.R0, Z_centre=equi.ZX/equi.R0, normal=True)
        
        elif self.lineout_key == "AXP0":
            self.x_lineout = np.linspace(run.grid.xmin, run.grid.xmax, 100)
            self.y_lineout = equi.point_axis(x=self.x_lineout, R_centre=equi.R0/equi.R0, Z_centre=equi.Z0/equi.R0, normal=True)
            
        else:
            raise NotImplementedError(f"Lineout not recognised {lineout}")

        self.x_lineout, self.y_lineout = self.remove_off_grid_points(run, self.x_lineout, self.y_lineout)

        self.f, self.u = interpolate.splprep([self.x_lineout, self.y_lineout], s=1, per=False)
        self.x_interp, self.y_interp = interpolate.splev(np.linspace(0, 1, self.resolution), self.f)

        self.calculate_arc_length()
        # self.calculate_bilinear_matrix()
    
    @staticmethod
    def remove_off_grid_points(run, x_test, y_test):
        flux_surface, _ = FluxSurface(run=run)()
        flux_surface = run.grid.vector_to_matrix(flux_surface.flatten())

        x_test = np.array(x_test)
        y_test = np.array(y_test)

        row = np.searchsorted(run.grid.x_unique, x_test)-1
        col = np.searchsorted(run.grid.y_unique, y_test)-1

        z_test = flux_surface[col, row]
        z_test[np.logical_or(row==-1, col==-1)] = np.nan

        x_test = x_test[np.logical_not(np.isnan(z_test))]
        y_test = y_test[np.logical_not(np.isnan(z_test))]

        return x_test, y_test

    # def calculate_bilinear_matrix(self):
        
    #     indi = []
    #     indj = []
    #     val = []

    #     nz = 0
    #     for x, y in zip(self.x_interp, self.y_interp):
    #         indi.append(nz)

    #         neighbours, weighting = self.find_neighbours(x, y)
    
    # def find_neighbours(self, x, y):
        
    #     x_vector, y_vector = self.run.x, self.run.y
    #     x_matrix, y_matrix = self.run.x_unique, self.run.y_unique

    #     if ((x > x_matrix.min()) & (x <= x_matrix.max()) &
    #         (y > y_matrix.min()) & (y <= y_matrix.max())):
            
    #         i = np.searchsorted(x_matrix, x)-1
    #         j = np.searchsorted(y_matrix, y)-1
            
    #         p00 = np.where(np.logical_and((x_vector == x_matrix[i]), (y_vector == y_matrix[j])))
    #         p01 = np.where(np.logical_and((x_vector == x_matrix[i]), (y_vector == y_matrix[j+1])))
    #         p10 = np.where(np.logical_and((x_vector == x_matrix[i+1]), (y_vector == y_matrix[j])))
    #         p11 = np.where(np.logical_and((x_vector == x_matrix[i+1]), (y_vector == y_matrix[j+1])))

    #         x1, x2 = x_index[i:i + 2]
    #         y1, y2 = y_index[j:j + 2]
    #         z11, z12 = vector[j][i:i + 2]
    #         z21, z22 = values[j + 1][i:i + 2]

    #     return 
    #     (z11 * (x2 - x) * (y2 - y) +
    #             z21 * (x - x1) * (y2 - y) +
    #             z12 * (x2 - x) * (y - y1) +
    #             z22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1))
    
    def calculate_arc_length(self):

        self.arc_l = np.cumsum(np.insert(np.sqrt(np.diff(self.x_interp) ** 2 + np.diff(self.y_interp) ** 2), 0, 0.0))
        self.arc_length = self.arc_l[-1]
    
    def rho_values(self):
        flux_surface, _ = FluxSurface(run=self.run)()

        return self.shape_values(flux_surface.flatten())

    def plot_sample_line(self):
        # plt.scatter(self.x_lineout, self.y_lineout, label='_nolegend_')
        plt.plot(self.x_interp, self.y_interp, label=self.lineout_key)
    
    @property
    def x(self):
        return np.linspace(0, 1, self.resolution)
    
    def determine_slices(self, time_slice=slice(-1, None), toroidal_slice=slice(1), poloidal_slice=slice(None)):
        # Natural slicing
        # Default to use the last snap, the 0th plane, and all poloidal points
        return time_slice, toroidal_slice, poloidal_slice

    def bilinear_interpolate(self, x, y, values):
        x_index, y_index, values = self.grid.x_unique, self.grid.y_unique, values

        i = np.searchsorted(x_index, x) - 1
        j = np.searchsorted(y_index, y) - 1

        if np.any([
                i == 0,
                i >= values.shape[1] - 1,
                j == 0,
                j >= values.shape[0] - 1
            ]):
            # If the full stencil isn't available, return NaN
            return np.nan

        x1, x2 = x_index[i:i + 2]
        y1, y2 = y_index[j:j + 2]
        z11, z12 = values[j][i:i + 2]
        z21, z22 = values[j + 1][i:i + 2]

        return (z11 * (x2 - x) * (y2 - y) +
                z21 * (x - x1) * (y2 - y) +
                z12 * (x2 - x) * (y - y1) +
                z22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1))

    def shape_values(self, values):
        
        assert(values.ndim == 1)

        # interpolator = interpolate.LinearNDInterpolator((self.grid.x, self.grid.y), values)
        # z_interp = interpolator((self.x_interp, self.y_interp))
        shaped_values = self.grid.vector_to_matrix(values)

        z_interp = np.zeros_like(self.x_interp)

        for i, x, y in zip(range(len(z_interp)), self.x_interp, self.y_interp):
            z_interp[i] = self.bilinear_interpolate(x, y, shaped_values)

        return z_interp