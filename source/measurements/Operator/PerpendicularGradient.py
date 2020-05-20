from . import Operator
from source import np
from ..Result import VectorResult

class PerpendicularGradient(Operator):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def values(self, z):
        
        # Should only be operated on scalar fields. For vector fields either do component-wise or implement new operator
        assert(not(z.is_vector))
        z_values = z.values
        # Convert to 2D matrix
        shaped_values = self.run.grid.vector_to_matrix(z_values)

        # Calculate the gradient. Units should be correctly propagated (including 1/m for the gradient)
        gradient_R = np.gradient(shaped_values, self.run.grid.grid_spacing, axis=-1)
        gradient_Z = np.gradient(shaped_values, self.run.grid.grid_spacing, axis=-2)

        # Convert back to 1D vectors
        gradient_R = self.run.grid.matrix_to_vector(gradient_R)
        gradient_Z = self.run.grid.matrix_to_vector(gradient_Z)

        return VectorResult.poloidal_init_from_subarrays(R_array=gradient_R, Z_array=gradient_Z, run=z.run)