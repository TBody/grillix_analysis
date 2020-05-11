from source import np, unit_registry
from source.Variable import VectorResult
from source.Variable.DerivedVariable import DerivedVariable
from source.Variable.BaseVariable import ScalarPotential
from source.Operator import PerpendicularGradient

class ElectricField(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "Electric field"
        self.vector_variable = True
        self.scalar_potential = ScalarPotential(**kwargs)
        self.perpendicular_gradient = PerpendicularGradient(**kwargs)
        self.base_variables = [self.scalar_potential, self.perpendicular_gradient]
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Te0 / (self.normalisation.electron_charge * self.normalisation.R0)
        self.normalisation_factor = self.normalisation_factor.to('kilovolts/m')
        self.delta = self.normalisation.delta

    def values(self, **kwargs):

        potential_gradient = self.perpendicular_gradient(self.scalar_potential(**kwargs))
        
        if not(self.convert):
            # 1/delta factor from differentiating on R0-normalised grid 
            potential_gradient = potential_gradient / self.delta

        return self.check_units(-1 * potential_gradient)
