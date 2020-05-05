from source import Quantity, np, plt
from source.Run import Run
from source.shared import vector_like

from source.Variable import ScalarPotential
from source.Variable.dynamic_derived.ElectricField import ElectricField

run = Run('TCV_half/init_start')

scalar_potential = ScalarPotential(run=run)
efield = ElectricField(run=run)

values = scalar_potential()

print(values.shape)

shaped_values = run.grid.vector_to_matrix(values)

print(shaped_values.shape)

electric_field_R = -np.gradient(shaped_values, run.grid.grid_spacing_normalised, axis=-1) * (run.normalisation.delta**-1)
electric_field_Z = -np.gradient(shaped_values, run.grid.grid_spacing_normalised, axis=-2) * (run.normalisation.delta**-1)

print(electric_field_R.shape)
print(electric_field_Z.shape)

E = vector_like(values.shape, R_array=run.grid.matrix_to_vector(electric_field_R), Z_array=run.grid.matrix_to_vector(electric_field_Z))

print(E.shape)


E_shaped = run.grid.vector_to_matrix(E, shift=1)
print(E_shaped.shape)

efield_values = run.grid.vector_to_matrix(efield(), shift=1)


# print(np.nanmean(electric_field_R[0,0,:,:]/efield_values[...,0]))
# assert(np.allclose(electric_field_R[0,0,:,:], E_shaped[0,0,:,:,0]))
# assert(np.allclose(electric_field_R, E_shaped[...,0], equal_nan=True))
# assert(np.allclose(electric_field_Z, E_shaped[...,2], equal_nan=True))
# assert(np.allclose(electric_field_R, efield_values[...,0], equal_nan=True))

# plt.contour(run.grid.x_unique, run.grid.y_unique, shaped_values[0, 0, :, :])

# arrow_length = np.sqrt(electric_field_R[0,0,:,:]**2 + electric_field_Z[0,0,:,:]**2)
# plt.quiver(run.grid.x_unique, run.grid.y_unique, electric_field_R[0,0,:,:], electric_field_Z[0,0,:,:], arrow_length) #, np.sqrt(electric_field_R[0,0,:,:]**2 + electric_field_Z[0,0,:,:]**2))

fig, axs = plt.subplots(ncols=3, sharex=True, sharey=True)

axs[0].pcolormesh(run.grid.x_unique, run.grid.y_unique, electric_field_R[0,0,:,:])
axs[1].pcolormesh(run.grid.x_unique, run.grid.y_unique, E_shaped[0,0,:,:,0])
axs[2].pcolormesh(run.grid.x_unique, run.grid.y_unique, efield_values[0,0,:,:,0])

# axs[1].pcolormesh(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(E[0,0,:,0]))
# axs[1].pcolormesh(run.grid.x_unique, run.grid.y_unique, run.grid.vector_to_matrix(run.grid.matrix_to_vector(electric_field_R[0,0,:,:])))

plt.show()