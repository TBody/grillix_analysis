from source import Quantity, np, plt
from source.Run import Run

from source.Variable import ScalarPotential, VectorResult
from source.Variable.DerivedVariable.ElectricField import ElectricField

run = Run('TCV_half/init_start')

scalar_potential = ScalarPotential(run=run)
efield = ElectricField(run=run)

values = scalar_potential()

shaped_values = run.grid.vector_to_matrix(values)

electric_field_R = -1.0*np.gradient(shaped_values, run.grid.grid_spacing_normalised, axis=-1) * (run.normalisation.delta**-1)
electric_field_Z = -1.0*np.gradient(shaped_values, run.grid.grid_spacing_normalised, axis=-2) * (run.normalisation.delta**-1)

E = VectorResult.poloidal_init_from_subarrays(R_array=run.grid.matrix_to_vector(electric_field_R), Z_array=run.grid.matrix_to_vector(electric_field_Z), run=run)

E_shaped = run.grid.vector_to_matrix(E)

efield_values = run.grid.vector_to_matrix(efield())

# print(np.nanmean(electric_field_R[0,0,:,:]/efield_values[...,0]))
# assert(np.allclose(electric_field_R[0,0,:,:], E_shaped[0,0,:,:,0]))
# assert(np.allclose(electric_field_R, E_shaped[...,0], equal_nan=True))
# assert(np.allclose(electric_field_Z, E_shaped[...,2], equal_nan=True))
# assert(np.allclose(electric_field_R, efield_values[...,0], equal_nan=True))

# plt.contour(run.grid.x_unique, run.grid.y_unique, shaped_values[0, 0, :, :])

# arrow_length = np.sqrt(electric_field_R[0,0,:,:]**2 + electric_field_Z[0,0,:,:]**2)
# plt.quiver(run.grid.x_unique, run.grid.y_unique, electric_field_R[0,0,:,:], electric_field_Z[0,0,:,:], arrow_length) #, np.sqrt(electric_field_R[0,0,:,:]**2 + electric_field_Z[0,0,:,:]**2))

fig, axs = plt.subplots(ncols=4, sharex=True, sharey=True)

axs[0].pcolormesh(run.grid.x_unique, run.grid.y_unique, electric_field_R[0,0,:,:])
axs[1].pcolormesh(run.grid.x_unique, run.grid.y_unique, E_shaped[0,0,:,:,0])
axs[2].pcolormesh(run.grid.x_unique, run.grid.y_unique, efield_values[0,0,:,:,0])
axs[3].pcolormesh(run.grid.x_unique, run.grid.y_unique, efield_values.vector_magnitude[0,0,:,:])

# axs[1].pcolormesh(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(E[0,0,:,0]))
# axs[1].pcolormesh(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(run.grid.matrix_to_vector(electric_field_R[0,0,:,:])))

plt.show()