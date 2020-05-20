from source import np
from ...WrappedArray import VectorArray
from . import DerivedVariable
from ..BaseVariable import ScalarPotential
from source.measurements.Operator import PerpendicularGradient

class ElectricField(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Electric field"
        self.vector_variable = True
        self.scalar_potential = ScalarPotential(run=run)
        self.perpendicular_gradient = PerpendicularGradient(run=run)
        self.base_variables = [self.scalar_potential, self.perpendicular_gradient]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.Te0 / (self.normalisation.electron_charge * self.normalisation.R0)
        self.normalisation_factor = self.normalisation_factor.to('kilovolts/m')
        self.delta = self.normalisation.delta

    def values(self, **kwargs):

        potential_gradient = self.perpendicular_gradient(self.scalar_potential(**kwargs))
        
        if not(self.SI_units):
            # delta factor from differentiating on R0-normalised grid 
            potential_gradient = potential_gradient * self.delta

        return self.check_units(-1 * potential_gradient)
