from source import np
from source.Variable import VectorResult
from source.Variable.DerivedVariable import DerivedVariable, ElectricField
from source.Variable.EquilibriumVariable import MagneticFieldTor

class ExBVelocity(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "ExB velocity"
        self.electric_field = ElectricField(**kwargs)
        self.toroidal_magentic_field = MagneticFieldTor(**kwargs)
        
        self.base_variables = [self.electric_field, self.toroidal_magentic_field]

        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')

    def values(self, **kwargs):

        electric_field = self.electric_field(**kwargs)
        Btor = self.toroidal_magentic_field(**kwargs)
        magnetic_field = VectorResult.vector_from_subarrays(R_array=np.zeros_like(Btor), phi_array=Btor, Z_array=np.zeros_like(Btor))
        
        ExB = np.cross(electric_field.values, magnetic_field.values)
