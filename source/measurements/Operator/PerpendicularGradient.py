from . import Operator
from source import np
from ..WrappedArray import VectorArray

class PerpendicularGradient(Operator):
    
    def __init__(self, run=None):
        super().__init__(run=run)
    
    def __call__(self, values, units):
        
        # Should only be operated on scalar fields. For vector fields either do component-wise or implement new operator
        assert(not(values.is_vector))
        # Convert to 2D matrix
        shaped_values = self.run.grid.vector_to_matrix(values)*units
        
        # Calculate the gradient. Units should be correctly propagated (including 1/m for the gradient)
        gradient_R = np.gradient(shaped_values, self.run.grid.grid_spacing * self.run.normalisation.R0, axis=-1)
        gradient_Z = np.gradient(shaped_values, self.run.grid.grid_spacing * self.run.normalisation.R0, axis=-2)
        units *= 1/self.run.normalisation.R0

        # Convert back to dimensionless 1D vectors
        gradient_R = self.run.grid.matrix_to_vector((gradient_R/units).to('').magnitude)
        gradient_Z = self.run.grid.matrix_to_vector((gradient_Z/units).to('').magnitude)

        return VectorArray.poloidal(R_array=gradient_R, Z_array=gradient_Z), units