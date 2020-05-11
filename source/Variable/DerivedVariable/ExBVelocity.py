from source import np, Quantity
from source.Variable import VectorResult
from source.Variable.DerivedVariable import DerivedVariable, ElectricField
from source.Variable.EquilibriumVariable import MagneticFieldTor

class ExBVelocity(DerivedVariable):
    
    def __init__(self, **kwargs):
        self.title = "ExB velocity"
        self.vector_variable = True
        self.electric_field = ElectricField(**kwargs)
        self.toroidal_magentic_field = MagneticFieldTor(**kwargs)
        
        self.base_variables = [self.electric_field, self.toroidal_magentic_field]

        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')

    def values(self, **kwargs):

        electric_field = self.electric_field(**kwargs)
        Btor = self.toroidal_magentic_field(**kwargs)

        if self.convert:
            zero_array = Quantity(np.zeros_like(Btor), Btor.units)
        else:
            zero_array = np.zeros_like(Btor)

        magnetic_field = VectorResult.init_from_subarrays(
            R_array = zero_array,
            phi_array=Btor.values,
            Z_array = zero_array,
            run=self.run
        )
        
        ExB = np.cross(electric_field, magnetic_field)/magnetic_field.vector_magnitude[:,:,:, np.newaxis]**2

        return self.check_units(ExB)
