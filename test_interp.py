import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate
from ipdb import launch_ipdb_on_exception

def f(x, y):
    return np.sin(x) + np.cos(y)

def mesh_grid(xmin, xmax, ymin, ymax, nx, ny, ax):
    grid_x = np.linspace(xmin, xmax, num=nx)
    grid_y = np.linspace(ymin, ymax, num=ny)
    mesh_x, mesh_y = np.meshgrid(grid_x, grid_y)

    mesh_z = f(mesh_x, mesh_y)

    plot = ax.pcolormesh(grid_x, grid_y, mesh_z)
    plt.colorbar(plot, ax=ax)

    return mesh_x, mesh_y, mesh_z

def builtin_interp(input_x, input_y, input_z, xmin, xmax, ymin, ymax, nx, ny, ax):

    grid_x = np.linspace(xmin, xmax, num=nx)
    grid_y = np.linspace(ymin, ymax, num=ny)
    mesh_x, mesh_y = np.meshgrid(grid_x, grid_y)

    interpolator = interpolate.LinearNDInterpolator((input_x.flatten(), input_y.flatten()), input_z.flatten())
    mesh_z = interpolator((mesh_x.flatten(), mesh_y.flatten()))

    mesh_z = mesh_z.reshape(mesh_x.shape)

    plot = ax.pcolormesh(grid_x, grid_y, mesh_z)
    plt.colorbar(plot, ax=ax)

    return mesh_x, mesh_y, mesh_z

def bilinear_interpolate(x, y, grid_x, grid_y, values):
    assert(values.ndim == 2)
    assert(values.shape[1] == grid_x.size)
    assert(values.shape[0] == grid_y.size)

    if np.any([
        x < grid_x.min(),
        x > grid_x.max(),
        y < grid_y.min(),
        y > grid_y.max()
        ]):
        return np.nan
    
    i0 = np.searchsorted(grid_x, x, side='right') - 1
    i1 = min(i0 + 1, grid_x.size - 1)
    j0 = np.searchsorted(grid_y, y, side='right') - 1
    j1 = min(j0 + 1, grid_y.size - 1)

    dx0 = x - grid_x[i0]
    dy0 = y - grid_y[j0]
    dx1 = grid_x[i1] - x
    dy1 = grid_y[j1] - y

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

def loop_interp(input_x, input_y, input_z, xmin, xmax, ymin, ymax, nx, ny, ax):

    grid_x = np.linspace(xmin, xmax, num=nx)
    grid_y = np.linspace(ymin, ymax, num=ny)
    mesh_x, mesh_y = np.meshgrid(grid_x, grid_y)

    mesh_z = np.zeros(mesh_x.shape)

    for x, i in zip(grid_x, range(len(grid_x))):
        for y, j in zip(grid_y, range(len(grid_y))):
            mesh_z[j][i] = bilinear_interpolate(x, y, np.unique(input_x), np.unique(input_y), input_z)

    plot = ax.pcolormesh(grid_x, grid_y, mesh_z)
    plt.colorbar(plot, ax=ax)

    return mesh_x, mesh_y, mesh_z

def weightings_interpolate(x, y, grid_x, grid_y):
    
    assert(grid_x.ndim == 1)
    assert(grid_y.ndim == 1)
    assert(grid_x.size == grid_y.size)

    if np.any([
        x < grid_x.min(),
        x > grid_x.max(),
        y < grid_y.min(),
        y > grid_y.max()
        ]):
        return [0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]
    
    diff_x = x - grid_x
    diff_y = y - grid_y

    ix0 = np.nanargmin(np.where(diff_x >= 0, diff_x, np.nan))
    ix1 = np.nanargmax(np.where(diff_x <= 0, diff_x, np.nan))

    iy0 = np.nanargmin(np.where(diff_y >= 0, diff_y, np.nan))
    iy1 = np.nanargmax(np.where(diff_y <= 0, diff_y, np.nan))

    i00 = np.where(np.logical_and(grid_x[ix0] == grid_x, grid_y[iy0] == grid_y))[0][0]
    i01 = np.where(np.logical_and(grid_x[ix0] == grid_x, grid_y[iy1] == grid_y))[0][0]
    i10 = np.where(np.logical_and(grid_x[ix1] == grid_x, grid_y[iy0] == grid_y))[0][0]
    i11 = np.where(np.logical_and(grid_x[ix1] == grid_x, grid_y[iy1] == grid_y))[0][0]
    
    dx0 = x - grid_x[ix0]
    dy0 = y - grid_y[iy0]
    dx1 = grid_x[ix1] - x
    dy1 = grid_y[iy1] - y

    # print(grid_x[ix0], x, grid_x[ix1], grid_y[iy0], y, grid_y[iy1])
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

def make_matrix_interp(grid_x, grid_y, interp_x, interp_y):
    from scipy.sparse import csr_matrix
    assert(grid_x.ndim == 1)
    assert(grid_y.ndim == 1)
    assert(grid_x.size == grid_y.size)
    assert(interp_x.ndim == 1)
    assert(interp_y.ndim == 1)
    assert(interp_x.size == interp_y.size)

    nz = 0
    indi = []
    indj = []
    val  = []

    for l in range(interp_x.size):
        indi.append(nz)

        [i00, i10, i01, i11, w00, w10, w01, w11] = weightings_interpolate(interp_x[l], interp_y[l], grid_x, grid_y)

        for index, weight in zip([i00, i10, i01, i11], [w00, w10, w01, w11]):
            if weight > 0.0:
                nz += 1
                indj.append(index)
                val.append(weight)
    
    indi.append(nz)

    return csr_matrix((val, indj, indi), shape=(interp_x.size, grid_x.size))

def matrix_interp(input_x, input_y, input_z, xmin, xmax, ymin, ymax, nx, ny, ax):

    grid_x = np.linspace(xmin, xmax, num=nx)
    grid_y = np.linspace(ymin, ymax, num=ny)
    mesh_x, mesh_y = np.meshgrid(grid_x, grid_y)

    interp_matrix = make_matrix_interp(input_x.flatten(), input_y.flatten(), mesh_x.flatten(), mesh_y.flatten())

    mesh_z = interp_matrix * input_z.flatten()

    mesh_z = mesh_z.reshape(mesh_x.shape)

    plot = ax.pcolormesh(grid_x, grid_y, mesh_z)
    plt.colorbar(plot, ax=ax)

    return mesh_x, mesh_y, mesh_z

if __name__=="__main__":

    with launch_ipdb_on_exception():

        fig, axs = plt.subplots(squeeze=True, ncols=4)

        xmin = -5.0
        xmax = 5.0
        ymin = -3.0
        ymax = 2.0
        coarse_nx = 10
        coarse_ny = 9
        fine_nx = 100
        fine_ny = 100

        mx0, my0, mz0 = mesh_grid(xmin, xmax, ymin, ymax, coarse_nx, coarse_ny, axs[0])

        mx1, my1, mz1 = builtin_interp(mx0, my0, mz0, xmin, xmax, ymin, ymax, fine_nx, fine_ny, axs[1])

        mx2, my2, mz2 = loop_interp(mx0, my0, mz0, xmin, xmax, ymin, ymax, fine_nx, fine_ny, axs[2])

        mx3, my3, mz3 = matrix_interp(mx0, my0, mz0, xmin, xmax, ymin, ymax, fine_nx, fine_ny, axs[3])

        plt.show()

