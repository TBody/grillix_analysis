from source import np
from source.shared import Vector
from source.Variable.dynamic_derived import DerivedDynamicVariable
from source.Variable.dynamic_base import ScalarPotential

class ExBVelocity(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "ExB velocity"
        self.scalar_potential = ScalarPotential(**kwargs)
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = np.sqrt(self.normalisation.Te0/self.normalisation.Mi)
        self.normalisation_factor = self.normalisation_factor.to('kilometers/second')

    def update_run_values(self):
        self.check_base_variables([self.scalar_potential])

    def values(self, **kwargs):
        # 1/delta factor for differentiating on R0-normalised grid

        scalar_potential = self.scalar_potential.values(**kwargs)

        electric_field_R = -np.gradient(scalar_potential, self.run.grid.grid_spacing, axis=1) * (self.normalisation.delta **-1)
        electric_field_Z = -np.gradient(scalar_potential, self.run.grid.grid_spacing, axis=0) * (self.normalisation.delta **-1)

                        
