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

    def fetch_values(self, **kwargs):

        
        electric_field = self.dimensional_array(self.electric_field(**kwargs))
        Btor = self.dimensional_array(self.toroidal_magentic_field(**kwargs))

        zero_array = np.zeros_like(Btor)
        
        magnetic_field = Quantity(VectorArray.cylindrical(
            R_array = zero_array,
            phi_array=Btor.magnitude,
            Z_array = zero_array
        ), Btor.units)
        
        ExB = np.cross(electric_field, magnetic_field)/magnetic_field.vector_magnitude[:,:,:, np.newaxis]**2

        return self.normalised_VectorArray(ExB)
