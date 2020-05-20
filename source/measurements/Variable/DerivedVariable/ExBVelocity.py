from source import np, Quantity
from ...WrappedArray import VectorArray
from . import DerivedVariable, ElectricField
from ..EquilibriumVariable import MagneticFieldTor

class ExBVelocity(DerivedVariable):
    
    def __init__(self, run=None):
        title = "ExB velocity"
        self.vector_variable = True
        self.electric_field = ElectricField(run=run)
        self.toroidal_magentic_field = MagneticFieldTor(run=run)
        
        self.base_variables = [self.electric_field, self.toroidal_magentic_field]

        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')

    def values(self, **kwargs):

        electric_field = self.electric_field(**kwargs)
        Btor = self.toroidal_magentic_field(**kwargs)

        if self.SI_units:
            zero_array = Quantity(np.zeros_like(Btor), Btor.units)
        else:
            zero_array = np.zeros_like(Btor)

        magnetic_field = VectorArray.cylindrical(
            R_array = zero_array,
            phi_array=Btor.values,
            Z_array = zero_array
        )
        
        ExB = np.cross(electric_field, magnetic_field)/magnetic_field.vector_magnitude[:,:,:, np.newaxis]**2

        return self.check_units(ExB)
