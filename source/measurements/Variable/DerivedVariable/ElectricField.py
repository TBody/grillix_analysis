from source import np
from ...WrappedArray import VectorArray
from . import DerivedVariable
from ..BaseVariable import ScalarPotential
from source.measurements.Operator import PerpendicularGradient

class ElectricField(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electric field"
        self.vector_variable = True
        self.scalar_potential = ScalarPotential()
        self.perpendicular_gradient = PerpendicularGradient()
        self.base_variables = [self.scalar_potential, self.perpendicular_gradient]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return (self.normalisation.Te0 / (self.normalisation.electron_charge * self.normalisation.rho_s0)).to('kilovolts/m')

    def fetch_values(self, **kwargs):
        
        scalar_potential, scalar_potential_units = self.scalar_potential(**kwargs)
        
        potential_gradient, potential_gradient_units = self.perpendicular_gradient(scalar_potential, scalar_potential_units)
        
        return self.normalised_VectorArray(potential_gradient*potential_gradient_units)
        
