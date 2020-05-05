from source import np, unit_registry
from source.Variable import VectorResult
from source.Variable.dynamic_derived import DerivedDynamicVariable
from source.Variable.dynamic_base import ScalarPotential

class ElectricField(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "Electric field"
        self.vector_variable = True
        self.scalar_potential = ScalarPotential(**kwargs)
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Te0 / (self.normalisation.electron_charge * self.normalisation.R0)
        self.normalisation_factor = self.normalisation_factor.to('kilovolts/m')

    def update_run_values(self):
        self.check_base_variables([self.scalar_potential])
    
    def values(self, **kwargs):
        # 1/delta factor from differentiating on R0-normalised grid

        scalar_potential = self.scalar_potential.values(**kwargs)

        return self.calculate_values(scalar_potential, self.run.grid.grid_spacing_normalised, self.normalisation.delta)
    
    @unit_registry.wraps(None, (None, None, None, None))
    def calculate_values(self, scalar_potential, grid_spacing, delta):
        
        shaped_values = self.run.grid.vector_to_matrix(scalar_potential)

        electric_field_R = -np.gradient(shaped_values, grid_spacing, axis=-1) * (delta **-1)
        electric_field_Z = -np.gradient(shaped_values, grid_spacing, axis=-2) * (delta **-1)

        return VectorResult.poloidal_vector_from_subarrays(R_array=self.run.grid.matrix_to_vector(electric_field_R), Z_array=self.run.grid.matrix_to_vector(electric_field_Z))



